# API-Master---SPOTIFY-DATA

Project Overview
This project retrieves data from the Spotify API using the spotipy library. The script is designed to authenticate with the Spotify API and extract data from playlists, enabling you to gather detailed information about trending music. It also uses MySQL to store the retrieved data for further analysis.

Key Features

Authentication: The script authenticates with Spotify's API using Client Credentials Flow, retrieving an access token for secure API access.

Playlist Data Retrieval: Fetches metadata from trending Spotify playlists, including details like track names, artists, and more.

Data Storage: The retrieved data is stored in a MySQL database for future analysis or integration into other applications.

Key Functions

get_access_token(client_id, client_secret):

Authenticates with Spotify using client_id and client_secret to retrieve an access token.
Sends a request to the Spotify accounts API and returns the token if successful.

get_trending_playlist_data(playlist_ids, access_token):

Takes a list of playlist IDs and retrieves data using the Spotify API.
Loops through the playlists and gathers relevant information about tracks and artists.

Data Storage:

Uses MySQL to connect to a database and store the retrieved playlist data for further use.

Dependencies
Python 3.x

Requests: For handling HTTP requests to the Spotify API.

Spotipy: Python library for the Spotify Web API.

Pandas: Used for data manipulation.

MySQL: For database operations.
