import pandas as pd
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors

def load_clean_data(path):
    df = pd.read_csv(path, encoding="utf-8")
    return df

def build_knn_model(X, n_neighbors=5):
    knn = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')
    knn.fit(X)
    return knn

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
    X_cluster = cluster_df[features].values
    knn_cluster = build_knn_model(X_cluster, n_neighbors=top_n+1)

    # Find neighbors within the cluster
    song_vector = row[features].values
    distances, indices = knn_cluster.kneighbors(song_vector, n_neighbors=top_n+1)

    similar_songs = cluster_df.iloc[indices[0][1:]][["track_name", "artists"]]
    
    return similar_songs


if __name__ == "__main__":
    df = load_clean_data("data/clean_dataset.csv") # Load the clean dataset
    genre_dummies = pd.get_dummies(df["track_genre"], prefix="genre")
    df = pd.concat([df, genre_dummies], axis=1)

    features = ['tempo', 'valence', 'energy', 'key', 'danceability'] + list(genre_dummies.columns)
    
    
    X = df[features].values
    
    kmeans = KMeans(n_clusters=10, random_state=42)
    labels = kmeans.fit_predict(X)
    
    df["cluster"] = labels
    
    df.to_csv("data/clean_tracks_with_clusters.csv", index=False, encoding="utf-8-sig")
