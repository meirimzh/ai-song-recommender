import numpy as np
import os
import json
import pandas as pd
from datetime import datetime
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from feedback import store_feedback,update_weight_from_feedback

Log_file = os.path.join(os.path.dirname(__file__),"recommendation_log.json")


def load_clean_data(path):
    df = pd.read_csv(path, encoding="utf-8")
    return df

def build_knn_model(X, n_neighbors=5): 
    knn = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')
    knn.fit(X)
    return knn

def apply_feature_weights(df_subset, features,weights_dict):
    weighted = df_subset[features].copy()
    for feat in weights_dict:
        if feat in weighted.columns:
            weighted[feat]*=weights_dict[feat] #multiplies each feature by its corresponding weights
    return weighted


def find_similar_songs(song_name, artist_name, df, features, top_n=5):
    song_name_clean = song_name.strip().lower()
    artist_name_clean = artist_name.strip().lower()
    
    df["track_name_clean"] = df["track_name"].str.strip().str.lower() #convert to lowercase and remove any whitespace
    df["artists_name_clean"] = df["artists"].str.strip().str.lower()

    row = df[
        (df["track_name_clean"] == song_name_clean) &
        (df["artists_name_clean"] == artist_name_clean)
    ]

    if row.empty:
        print("Song not found!")
        return None

    # Find the song's cluster
    song_cluster = int(row["cluster"].values[0])
    cluster_df = df[df["cluster"] == song_cluster]
   
    cluster_df_weighted = apply_feature_weights(cluster_df,features,feature_weight)
    row_weighted = apply_feature_weights(row,features,feature_weight)
 
    for feature in feature_weight:
        if feature in cluster_df_weighted.columns:
            cluster_df_weighted[feature] = cluster_df_weighted[feature]*feature_weight[feature]
            row_weighted[feature] = row_weighted[feature]*feature_weight[feature]
        
    X_cluster = cluster_df_weighted.values
    song_vector=row_weighted.values
    
    knn_cluster = build_knn_model(X_cluster, n_neighbors=top_n+1)
    
    # Find neighbors within the cluster
    distances, indices = knn_cluster.kneighbors(song_vector, n_neighbors=top_n+1)

    similar_songs = cluster_df.iloc[indices[0][1:]][["track_name", "artists"]]#exclude input song
    
    return similar_songs

def log_recommendation(input_songs, recommended_songs):
    log_entry ={
        "timestamp":datetime.now().isoformat(),
        "input song":input_songs,
        "recommended_songs":recommended_songs
    }
    
    if os.path.exists(Log_file):
        with open(Log_file,"r") as f:
            logs = json.load(f)
    else:
        logs=[]
    
    logs.append(log_entry)
    
    with open(Log_file,"w") as f:
        json.dump(logs,f,indent=2)


if __name__ == "__main__":
    df = load_clean_data("data/clean_dataset.csv") # Load the clean dataset
    genre_dummies = pd.get_dummies(df["track_genre"], prefix="genre")
    df = pd.concat([df, genre_dummies], axis=1)

    #gets the path to weights.json
    base_path = os.path.dirname(__file__)
    weights_path = os.path.join(base_path,"weights.json")

    base_features = ['tempo', 'valence', 'energy', 'danceability', 'acousticness','loudness']
    features = base_features+list(genre_dummies.columns)
    
    with open(weights_path  ,"r") as f:
        feature_weight = json.load(f) #loads the weights
        
    weights= np.array([feature_weight.get(feat,1.0) for feat in features])#retreives weights, default is set to 1.0 if missing
    X = df[features].values

    #multiply feature values by their weights
    X_weighted = X * weights
    
    
    kmeans = KMeans(n_clusters=10, random_state=42)
    labels = kmeans.fit_predict(X)
    df["cluster"] = labels
    
    df.to_csv("data/clean_tracks_with_clusters.csv", index=False, encoding="utf-8-sig")
 
    #test
    song_name = input("enter song name:").strip().lower()
    artist_name = input("enter the name of the artist:").strip().lower()
    
    similar = find_similar_songs(song_name, artist_name, df, features, top_n=5)
    
    if similar is not None:
        print(f"\nSimilar songs to: {song_name} by {artist_name}")
        print(similar)
        
        input_song = f"{song_name}-{artist_name}"
        recommended_list=similar[["track_name","artists"]].values.tolist()
        formatted_recommendations = [f"{title} -{artist}" for title, artist in recommended_list]
        log_recommendation(input_song,formatted_recommendations)
        
        print("\nFeature weights applied:")
        for feat, weight in feature_weight.items():
            print(f"{feat}: {weight:.7f}")

        try:
            rating = int(input("\nPlease rate the recommendation from 1 to 5: "))
            if 1<= rating<= 5:
                input_song = f"{song_name} - {artist_name}"
                store_feedback(input_song,rating,feature_weight)
                print("feedback saved")
            else:
                print("rating must be between 1 and 5, feedback skipped")
        except ValueError:
            print("invalid input, feed back skipped")
            
        update = input("do u want to update weights now> (y/n): ").strip().lower()
        if update == 'y':
            update_weight_from_feedback()
            
        
