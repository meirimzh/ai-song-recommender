import pandas as pd
from sklearn.preprocessing import StandardScaler

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
        'key',
        'track_genre',
        'danceability'
    ]
    df = df[features]
    
    df = df.dropna() #removes any rows with a missing value

    
    df = df.drop_duplicates(subset=['track_name', 'artists']) # Drops duplicate songs

   
    numeric_cols = ['tempo', 'valence', 'energy','key','danceability']  
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    df.to_csv(output_path, index=False, encoding = "utf-8-sig")
    print(f"Saved cleaned data to {output_path}")
    
if __name__ == "__main__":
    clean_and_process_data(
        input_path='data/tracks_dataset.csv',
        output_path='data/clean_dataset.csv'
    )
