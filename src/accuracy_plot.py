import json
import matplotlib.pyplot as plt
from datetime import datetime

def normalize_song_name(name):
    return name.lower().replace(" ", "").replace("-", "")

# Loads recommendation log
with open("src/recommendation_log.json", "r") as f:
    recommendation_log = json.load(f)

# Loads feedback log
with open("src/feedback_log.json", "r") as f:
    feedback_log = json.load(f)

song_to_time = {}
for entry in recommendation_log:
    input_song = entry.get("input song") 
    if input_song:
        key = normalize_song_name(input_song)
        timestamp = entry.get("timestamp") 
        if timestamp:
            song_to_time[key] = datetime.fromisoformat(timestamp.strip())


timestamps = []
ratings = []

for entry in feedback_log:
    song = entry.get("song")
    rating = entry.get("rating")
    if song and rating is not None:
        key = normalize_song_name(song)
        time = song_to_time.get(key)
        if time:
            timestamps.append(time)
            ratings.append(rating)

# Plotting
plt.figure(figsize=(8, 5))
plt.plot(timestamps, ratings, marker='o', linestyle='-', color='hotpink')
plt.title("Ratings Over Time")
plt.xlabel("Timestamp")
plt.ylabel("Rating")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
