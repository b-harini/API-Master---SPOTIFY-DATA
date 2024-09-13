import requests
import base64
from pymysql import connect
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_access_token(client_id, client_secret):
    """Get access token using client ID and client secret."""
    client_credentials = f"{client_id}:{client_secret}"
    client_credentials_base64 = base64.b64encode(client_credentials.encode())

    token_url = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': f'Basic {client_credentials_base64.decode()}'}
    data = {'grant_type': 'client_credentials'}
    response = requests.post(token_url, data=data, headers=headers)

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print("Error obtaining access token.")
        exit()

def get_trending_playlist_data(playlist_ids, access_token):
    """Retrieve data from Spotify playlists."""
    sp = spotipy.Spotify(auth=access_token)
    music_data = []

    for playlist_id in playlist_ids:
        playlist_tracks = sp.playlist_tracks(playlist_id, fields='items(track(id, name, artists, album(id, name)))')

        for track_info in playlist_tracks['items']:
            track = track_info['track']
            track_name = track['name']
            artists = ', '.join([artist['name'] for artist in track['artists']])
            album_name = track['album']['name']
            album_id = track['album']['id']
            track_id = track['id']

            audio_features = sp.audio_features(track_id)[0] if track_id != 'Not available' else None

            try:
                album_info = sp.album(album_id) if album_id != 'Not available' else None
                release_date = album_info['release_date'] if album_info else None
            except:
                release_date = None

            try:
                track_info = sp.track(track_id) if track_id != 'Not available' else None
                popularity = track_info['popularity'] if track_info else None
            except:
                popularity = None

            track_data = {
                'Track Name': track_name,
                'Artists': artists,
                'Album Name': album_name,
                'Album ID': album_id,
                'Track ID': track_id,
                'Popularity': popularity,
                'Release Date': release_date,
                'Duration (ms)': audio_features['duration_ms'] if audio_features else None,
                'Explicit': track_info.get('explicit', None),
                'External URLs': track_info.get('external_urls', {}).get('spotify', None),
                'Danceability': audio_features['danceability'] if audio_features else None,
                'Energy': audio_features['energy'] if audio_features else None,
                'Key': audio_features['key'] if audio_features else None,
                'Loudness': audio_features['loudness'] if audio_features else None,
                'Mode': audio_features['mode'] if audio_features else None,
                'Speechiness': audio_features['speechiness'] if audio_features else None,
                'Acousticness': audio_features['acousticness'] if audio_features else None,
                'Instrumentalness': audio_features['instrumentalness'] if audio_features else None,
                'Liveness': audio_features['liveness'] if audio_features else None,
                'Valence': audio_features['valence'] if audio_features else None,
                'Tempo': audio_features['tempo'] if audio_features else None,
            }
            music_data.append(track_data)

    df = pd.DataFrame(music_data)
    return df

def upload_to_database(df, host, user, password, database_name, table_name):
    """Upload data to MySQL database."""
    database = connect(host=host, user=user, password=password, database=database_name)
    cur = database.cursor()
    
    query = f"INSERT INTO {table_name} (track_name, artists, album_name, album_id, track_id, popularity, release_date, duration_ms, explicit, external_urls, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    # Adjust the values list comprehension to match the column names in your DataFrame
    values = [(row['Track Name'], row['Artists'], row['Album Name'], row['Album ID'], row['Track ID'], row['Popularity'], row['Release Date'], row['Duration (ms)'], row['Explicit'], row['External URLs'], row['Danceability'], row['Energy'], row['Key'], row['Loudness'], row['Mode'], row['Speechiness'], row['Acousticness'], row['Instrumentalness'], row['Liveness'], row['Valence'], row['Tempo']) for _, row in df.iterrows()]  
    
    cur.executemany(query, values)
    database.commit()
    cur.close()
    database.close()
    print("Data upload complete.")


def main():
    CLIENT_ID = 'XXXXXXXXXXXXXXXXX'
    CLIENT_SECRET = 'XXXXXXXXXXXXXX'
    playlist_ids = ['37i9dQZF1EIgzSCNweQzPQ', '37i9dQZF1DX70RN3TfWWJh', '2o9hPqsW5HoxVFAdUDfD6K']  # Example playlist IDs
    host = 'localhost'
    user = 'root'
    password = 'rootroot'
    database_name = 'mysql'
    table_name = 'spotify'
    
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    music_df = get_trending_playlist_data(playlist_ids, access_token)
    upload_to_database(music_df, host, user, password, database_name, table_name)

if __name__ == "__main__":
    main()
