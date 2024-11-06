import pydgraph
import json

def create_dgraph_client():
    """Crea un cliente de Dgraph y se conecta al servidor."""
    client_stub = pydgraph.DgraphClientStub('localhost:9080')
    client = pydgraph.DgraphClient(client_stub)
    return client

def query_playlist_tracks(client, user_id, playlist_name):
    """Consulta las canciones en una playlist específica de un usuario."""
    query = f"""
    {{
      var(func: eq(user_id, "{user_id}")) {{
        playlists := creates @filter(eq(playlist_name, "{playlist_name}")) {{
          tracks_in_playlist as includes {{
            uid
          }}
        }}
      }}

      tracks_in_playlist(func: uid(tracks_in_playlist)) {{
        track_id
        track_name
        performed_by {{
          artist_name
        }}
      }}
    }}
    """
    try:
        response = client.txn(read_only=True).query(query)
        tracks = json.loads(response.json())
        print("Query successful. Tracks in Playlist:", tracks)
    except Exception as e:
        print("Failed to query playlist tracks:", e)

def query_recommended_tracks(client, user_id, playlist_name):
    """Consulta recomendaciones de canciones que no están en la playlist especificada."""
    query = f"""
    {{
      var(func: eq(user_id, "{user_id}")) {{
        playlists := creates @filter(eq(playlist_name, "{playlist_name}")) {{
          tracks_in_playlist as includes {{
            uid
          }}
        }}
      }}

      recommended_tracks(func: type(Track)) @filter(NOT uid(tracks_in_playlist)) {{
        track_id
        track_name
        performed_by {{
          artist_name
        }}
      }}
    }}
    """
    try:
        response = client.txn(read_only=True).query(query)
        recommended_tracks = json.loads(response.json())
        print("Query successful. Recommended Tracks:", recommended_tracks)
    except Exception as e:
        print("Failed to query recommended tracks:", e)

def main():
    client = create_dgraph_client()
    user_id = "your-user-id"  # Replace with the actual user ID
    playlist_name = "your-playlist-name"  # Replace with the actual playlist name

    print("Querying tracks in the playlist...")
    query_playlist_tracks(client, user_id, playlist_name)

    print("Querying recommended tracks not in the playlist...")
    query_recommended_tracks(client, user_id, playlist_name)

if __name__ == '__main__':
    main()
