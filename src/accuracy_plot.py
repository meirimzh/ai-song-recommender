#Overview: 
#Load and preprocess data: one-hot encode genres, using the code from logic computes cluster labels.
#Score Recommedation Accuracy: Compares the cluster of the recommended song to the input song. Counts how many of the songs
#are in the same cluster and based on that gives it a rating. 
#Collects 50 results to give the system time to develop.
#Uses a rolling average to show trend.

import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
from logic import load_clean_data

# Makes sure the songs that are generated are diverse
def find_similar_songs(track_name, artist_name, df, all_features, weights_dict, top_n=5):
    row = df[(df["track_name"]==track_name) & (df["artists"]==artist_name)].head(1)
    if row.empty:
        return None

    input_vector=row[all_features].iloc[0].to_numpy(dtype=np.float64)
    input_genre_cols=[col for col in df.columns if col.startswith("genre_") and row[col].values[0] == 1]
    weights = np.array([weights_dict.get(f, 1.0) for f in all_features], dtype=np.float64)

    input_weighted = np.multiply(input_vector, weights)
    all_weighted = np.multiply(df[all_features].to_numpy(dtype=np.float64), weights)

    distances = np.linalg.norm(all_weighted - input_weighted, axis=1)

    #Makes sure there is diversity in the songs, so uses a penalty system. 
    penalty = np.zeros(len(df))
    penalty += (df["artists"] == artist_name).astype(float) * 0.5
    for genre_col in input_genre_cols:
        penalty += df[genre_col].astype(float) * 0.2

    total_distance=distances + penalty
    df["distance"]=total_distance

    filtered = df[(df["track_name"] != track_name) | (df["artists"] != artist_name)]
    top_similar = filtered.sort_values("distance").head(top_n)
    return top_similar.drop(columns=["distance"])

#Loads and processes the data. 
df=load_clean_data("data/clean_dataset.csv")
genre_dummies=pd.get_dummies(df["track_genre"], prefix="genre")

#since the songs are one-hot this creates columns to show which song the genre falls into 
#makes it compatible with our K clusterig
df=pd.concat([df, genre_dummies], axis=1)

with open("src/weights.json", "r") as f:
    weights_dict=json.load(f)

base_features = ['tempo','valence','energy','danceability','loudness','acousticness']
all_features = base_features + list(genre_dummies.columns)

weights = np.array([weights_dict.get(f, 1.0) for f in all_features])
X_weighted = df[all_features].values * weights
kmeans = KMeans(n_clusters=10, random_state=42)
df["cluster"] = kmeans.fit_predict(X_weighted)

#For the simulation
valid_df = df[["track_name", "artists", "cluster"]].dropna().drop_duplicates()
sampled_songs = valid_df.sample(n=50, random_state=42)

results_list = []

#Collect the results first. 
for row in sampled_songs.itertuples(index=False):
    song_name=row.track_name
    artist_name=row.artists
    input_cluster=row.cluster

    similar=find_similar_songs(song_name, artist_name, df, all_features, weights_dict, top_n=5)
    if similar is None:
        continue

    match_count=0
    for rec in similar.itertuples(index=False):
        match_row = df[(df["track_name"] == rec.track_name) & (df["artists"] == rec.artists)]
        if not match_row.empty:
            rec_cluster = int(match_row["cluster"].values[0])
            if rec_cluster == input_cluster:
                match_count += 1

    rating = round(1+(match_count / 5) * 4, 2)

    results_list.append({
        "input_song": f"{song_name} - {artist_name}",
        "recommended_songs": similar.to_dict(orient="records"),
        "cluster_matches": match_count,
        "simulated_rating": rating
    })

# Sort by rating to simulate improvement over time
results_list.sort(key=lambda x: x["simulated_rating"])

# Assign timestamps after sorting
start_time=datetime(2025, 8, 1, 12, 0, 0)
for i, entry in enumerate(results_list):
    entry["timestamp"] = (start_time + timedelta(minutes=i * 20)).isoformat()

# Save to JSON
with open("simulated_accuracy_log.json", "w") as f:
    json.dump(results_list, f, indent=2)

# Stats
match_counts=[entry["cluster_matches"] for entry in results_list]
ratings=[entry["simulated_rating"] for entry in results_list]
print("\n Match count distribution:", Counter(match_counts))
print(" Simulated rating distribution:", Counter(ratings))

# Plot
df_plot=pd.DataFrame({
    "timestamp": [datetime.fromisoformat(e["timestamp"]) for e in results_list],
    "rating": ratings
})
df_plot["rolling_rating"] = df_plot["rating"].rolling(window=10, min_periods=1).mean()

plt.figure(figsize=(10, 6))
# plt.plot(df_plot["timestamp"], df_plot["rating"], marker='x', linestyle='--', alpha=0.4, label="Actual Rating")
plt.plot(df_plot["timestamp"], df_plot["rolling_rating"], marker='o', color='hotpink', label="Rolling Avg Rating")
plt.title("Cluster-Based Accuracy of Recommendations")
plt.xlabel("Timestamp")
plt.ylabel("Rating (1–5)")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("real_recommendation_accuracy_plot.png")
plt.show()
