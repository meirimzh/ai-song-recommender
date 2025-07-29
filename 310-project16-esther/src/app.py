from flask import Flask, request, jsonify, send_from_directory
import os
import json
import pandas as pd

from logic import (find_similar_songs, log_recommendation)


BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
weights_path = os.path.join(BASE_DIR, "weights.json")
data_path = os.path.join(BASE_DIR, "..", "data", "clean_tracks_with_clusters.csv")
log_file = os.path.join(BASE_DIR,"recommendation_log.json")

#serving files from frontend
app = Flask(__name__, static_folder = FRONTEND_DIR, static_url_path='') 

df = pd.read_csv(data_path, encoding="utf-8-sig")

#loading feature weights
with open(weights_path, "r") as f:
    feature_weight = json.load(f)

base_features = ['tempo', 'valence', 'energy', 'danceability']
genre_dummies = [col for col in df.columns if col.startswith("genre_")]
features = base_features + genre_dummies

@app.route('/')
def frontend_run():
    return send_from_directory(app.static_folder, "home.html")

@app.route('/similar', methods=['POST'])
def similar():
    data = request.json #expeted output
    song_name = data.get('song')
    artist_name = data.get('artist')

    if not song_name or not artist_name:
        return jsonify({"error": "Missing song name or artist name"}), 400

    similar = find_similar_songs(song_name, artist_name, df, features, feature_weight)

    if similar is None:
        return jsonify({"error": "Song not found"}), 404

    recommendations = similar[["track_name", "artists"]].values.tolist()
    formatted = [f"{title} - {artist}" for title, artist in recommendations]

    input_song = f"{song_name} - {artist_name}"
    log_recommendation(input_song, formatted, log_file) #adding the calls to the log_recommendation file

    return jsonify({"recommendations": formatted})

if __name__ == "__main__":
    app.run(port = 5000)


