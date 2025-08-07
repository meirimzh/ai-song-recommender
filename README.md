# AI Similar Song Generator

Our AI system is as a tool that finds songs based on the user’s interests. The system takes song and artist names as an input from the user, and outputs similar songs based on our chosen features (bpm, key, genre, etc.) so that the user has a chance to discover new songs that have the similar vibes to their favorite ones.

**To test our system:**

1. Open the project in VSCode
2. Open 2 split terminals
3. On the first terminal, run python src/app.py to connect to the localhost that will receive song recommendation requests from the frontend
4. Make sure that you have Electron and Flask installed in your system
5. On the second terminal, run npm start to open the Electron-based UI
6. Press “Start finding new songs”

DISCLAIMER‼️:
  Our dataset might not have the songs/artists that you might want to enter, so either:

  Check that your song/artist is included in the dataset by opening data/clean_tracks_with_clusters.csv, and looking up the names using “Ctrl + F" before testing the system

  OR

  You can test the system with one of these songs:

	  “It will rain” - Bruno Mars
	  “Bad romance” - Lady Gaga
	  “Boyfriend” - Ariana Grande;Social House

  If your song has multiple artists, format it like “artist1;artist2”

7. Enter song and artist names
8. Press “Get Recommendations”
9. After seeing and evaluating the songs, please make sure to rate the recommendations by pressing on the according number of hearts

<p align="center">
‼️Please reopen the UI using npm start if you face any issues with the system‼️
</p>
<p align="center">
Thank you for testing our system!
</p>

