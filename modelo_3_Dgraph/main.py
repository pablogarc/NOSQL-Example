import pydgraph
import pandas as pd
import json
import uuid
from faker import Faker
import random
from datetime import datetime

fake = Faker()


def create_dgraph_client():
    client_stub = pydgraph.DgraphClientStub("localhost:9080")
    client = pydgraph.DgraphClient(client_stub)
    return client


def data_handler():
    df = pd.read_csv("spotify-2023.csv", encoding="iso-8859-1")
    df.rename(columns={"artist(s)_name": "artist"}, inplace=True)
    df.columns = df.columns.str.replace("_%", "")
    df.drop(
        [
            "in_apple_playlists",
            "in_apple_charts",
            "in_deezer_playlists",
            "in_deezer_charts",
            "in_shazam_charts",
            "released_year",
            "released_month",
            "released_day",
            "in_spotify_playlists",
            "in_spotify_charts",
        ],
        axis=1,
        inplace=True,
    )
    df.dropna(inplace=True)
    df["track_id"] = [str(uuid.uuid4()) for _ in range(len(df.index))]
    cols = list(df.columns)
    cols = [cols[-1]] + cols[:-1]
    df = df[cols]
    df["artist"] = df["artist"].str.split(", ")
    df["artist_count"] = df["artist"].apply(len)
    df["artist_1"] = df["artist"].apply(lambda x: x[0])
    df["artist_2"] = df["artist"].apply(lambda x: x[1] if len(x) > 1 else None)
    df["artist_3"] = df["artist"].apply(lambda x: x[2] if len(x) > 2 else None)
    df.drop(["artist", "artist_count"], axis=1, inplace=True)
    return df


def set_schema(client):
    schema = """
        type User {
            user_id
            user_name
        }

        type Track {
            track_id
            track_name
            streams
            bpm
            key
            mode
            danceability
            valence
            energy
            acousticness
            instrumentalness
            liveness
            speechiness
        }

        type Artist {
            artist_id
            artist_name
        }

        type Playlist {
            playlist_id
            playlist_name
            creation_date
        }

        user_id: string @index(exact) .
        user_name: string @index(fulltext) .

        track_id: string @index(exact) .
        track_name: string @index(term) .
        streams: int .
        bpm: int .
        key: string .
        mode: string .
        danceability: float .
        valence: float .
        energy: float .
        acousticness: float .
        instrumentalness: float .
        liveness: float .
        speechiness: float .

        artist_id: string @index(exact) .
        artist_name: string @index(term) .

        playlist_id: string @index(exact) .
        playlist_name: string @index(term) .
        creation_date: datetime @index(day) .

        listens: [uid] @reverse @count .
        performed_by: [uid] @reverse .
        creates: [uid] @reverse .
        includes: [uid] @reverse .

        listen_count: int .
        last_listened: datetime .
    """

    try:
        client.alter(pydgraph.Operation(schema=schema))
        print("Schema set successfully.")
    except Exception as e:
        print("Failed to set schema:", e)


def generateUser():
    user_id = str(uuid.uuid4())
    name = fake.name()
    return {"id": user_id, "name": name}


def generateArtist(artist_name):
    artist_id = str(uuid.uuid4())
    return {"id": artist_id, "name": artist_name}


def generatePlaylist(playlist_name="Default Playlist"):
    playlist_id = str(uuid.uuid4())
    year = random.randint(2015, 2023)
    date = fake.date_between_dates(
        date_start=datetime(year, 1, 1), date_end=datetime(year, 12, 31)
    )
    return {"id": playlist_id, "name": playlist_name, "date": date}


def generate_track(df):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("El input debe ser un DataFrame de pandas.")
    df["track_id"] = [str(uuid.uuid4()) for _ in range(len(df))]
    return df


def generate_artist_entities(df):
    required_columns = ["artist_1", "artist_2", "artist_3"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Faltan las siguientes columnas requeridas en el DataFrame: {', '.join(missing_columns)}"
        )

    artist_series = pd.concat(
        [df[col] for col in required_columns if col in df.columns]
    )
    artist_series.replace({None: pd.NA}, inplace=True)
    artist_series.dropna(inplace=True)

    unique_artists = artist_series.unique()

    artist_df = pd.DataFrame(
        {
            "artist_id": [str(uuid.uuid4()) for _ in range(len(unique_artists))],
            "artist_name": unique_artists,
        }
    )

    return artist_df


def load_data(client):
    data = data_handler()
    successful_loads = 0
    failed_loads = 0
    for index, row in data.iterrows():
        mutation = pydgraph.Mutation(set_json=json.dumps(row.to_dict()).encode("utf-8"))
        txn = client.txn()
        try:
            txn.mutate(mutation)
            txn.commit()
            successful_loads += 1
        except Exception as e:
            print(f"Failed to load data for track {row['track_id']}: {e}")
            failed_loads += 1
        finally:
            txn.discard()
    print(
        f"Data loading complete. Successful: {successful_loads}, Failed: {failed_loads}"
    )


def create_artists(artists):
    txn = client.txn()
    try:
        for artist in artists:
            artist_data = {
                "uid": "_:{}".format(str(uuid.uuid4())),
                "artist_id": str(uuid.uuid4()),
                "artist_name": artist,
            }
            txn.mutate(set_obj=artist_data)
        txn.commit()
    finally:
        txn.discard()


def create_tracks(tracks):
    txn = client.txn()
    try:
        for track in tracks:
            track_data = {
                "uid": "_:{}".format(str(uuid.uuid4())),
                "track_id": str(uuid.uuid4()),
                "track_name": track["name"],
                "streams": track["streams"],
                "bpm": track["bpm"],
                "key": track["key"],
                "mode": track["mode"],
                "danceability": track["danceability"],
                "valence": track["valence"],
                "energy": track["energy"],
                "acousticness": track["acousticness"],
                "instrumentalness": track["instrumentalness"],
                "liveness": track["liveness"],
                "speechiness": track["speechiness"],
            }
            txn.mutate(set_obj=track_data)
        txn.commit()
    finally:
        txn.discard()


def set_performed_by(track_uid, artist_uid):
    txn = client.txn()
    try:
        relation_data = {"uid": track_uid, "performed_by": {"uid": artist_uid}}
        txn.mutate(set_obj=relation_data)
        txn.commit()
    finally:
        txn.discard()


def set_listens(user_uid, track_uid, listen_count, last_listened):
    txn = client.txn()
    try:
        relation_data = {
            "uid": user_uid,
            "listens": [
                {
                    "uid": track_uid,
                    "listen_count": listen_count,
                    "last_listened": last_listened,
                }
            ],
        }
        txn.mutate(set_obj=relation_data)
        txn.commit()
    finally:
        txn.discard()


def main():
    client = create_dgraph_client()
    set_schema(client)
    load_data(client)


if __name__ == "__main__":
    main()
