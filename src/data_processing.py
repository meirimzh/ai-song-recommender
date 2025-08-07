import pandas as pd
import re
from sklearn.preprocessing import StandardScaler

def clean_track_name(song_name):
    song_name = song_name.lower().strip()
    song_name=re.sub(r'\(.*?\)','',song_name) #remove anything in ()
    song_name = re.sub(r'\[.*?\]', '', song_name)#remove anythin in []  
    song_name=re.split(r'\b(ft\.?|feat\.?|featuring)\b',song_name)[0]
    song_name = song_name.split(' - ')[0] #removes everything after a dash
    return song_name.strip()

def clean_and_process_data(input_path, output_path):
    df = pd.read_csv(input_path, encoding="utf-8-sig") #encoding to detect non english characters
    df.columns = df.columns.str.strip()

    #features chosen
    features = [
        'track_name',
        'artists',
        'tempo',
        'valence',
        'energy',
        'track_genre',
        'danceability',
        'loudness', 
        'acousticness'
    ]
    df = df[features]
    
    df = df.dropna() #removes any rows with a missing value

    
    df['track_name'] = df['track_name'].apply(clean_track_name)
    df['artists'] = df['artists'].str.lower().str.strip()    
    df = df.drop_duplicates(subset=['track_name', 'artists']) # Drops duplicate songs

   
    numeric_cols = ['tempo', 'valence', 'energy','danceability', 'loudness', 'acousticness']  
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    df.to_csv(output_path, index=False, encoding = "utf-8-sig")
    print(f"Saved cleaned data to {output_path}")
    
if __name__ == "__main__":
    clean_and_process_data(
        input_path='data/tracks_dataset.csv',
        output_path='data/clean_dataset.csv'
    )
