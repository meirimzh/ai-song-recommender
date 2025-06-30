import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logic import load_clean_data, find_similar_songs

def main():
    df = load_clean_data("data/clean_tracks_with_clusters.csv")

    genre_dummies = pd.get_dummies(df["track_genre"], prefix="genre")
    df = pd.concat([df, genre_dummies], axis=1)

    features = [
        'tempo',
        'valence',
        'energy',
        'key',
        'danceability'
    ] + list(genre_dummies.columns)

    song_name = input("Song name: ").strip()
    artist_name = input("Artist name: ").strip()
   
    similar = find_similar_songs(song_name, artist_name, df, features, top_n = 5)
    if similar is not None:
        print("Similar songs to:", song_name)
        print(similar)
    else:
        print("No similar songs found")

if __name__ == "__main__":
    main()
