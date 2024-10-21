import json
import logging
import pandas as pd
from dotenv import dotenv_values
from utils import utils, db

### Set up config and credentials ###
logger = logging.getLogger(__name__)
utils.set_logger()

#Config
db_cred = dotenv_values("credentials/db-cred.env")

#Parameters
db_name = "spotify"
schema_name = "playlist"

def main():
    with open("top_50_sg.json") as f:
        playlist = json.load(f)
    
    tracks = playlist["items"]
    track = tracks[0]

    #Artists
    table_name = "artists"

    artist_details = track["track"]["artists"]
    num_of_artists = len(artist_details)
    artists_values = [0] * num_of_artists
    for artist_no in range(num_of_artists):
        artist_row = (
            track["track"]["id"],
            artist_details[artist_no]["id"],
            artist_details[artist_no]["name"]
        )
        artists_values[artist_no] = artist_row

    artists_columns = '(track_id, artist_id, name)'

    pg_manager = db.PostgreManager(
        database = db_cred["database"],
        user = db_cred["user"],
        password = db_cred["password"],
        host = db_cred["host"],
        port = db_cred["port"]
        )
    conn = pg_manager.conn

    pg_manager.truncate_table(
        conn = conn,
        schema_name = schema_name,
        table_name = table_name
    )

    pg_manager.insert_table(
        conn = conn,
        schema_name = schema_name,
        table_name = table_name,
        table_columns = artists_columns,
        table_values = artists_values
    )
    df = pd.read_sql_query(f"SELECT * FROM {db_name}.{schema_name}.artists;", conn)
    print(df.head())


if __name__ == "__main__":
    main()