import json
import logging
from dotenv import dotenv_values
from utils import utils, db

### Set up config and credentials ###
logger = logging.getLogger(__name__)
utils.set_logger()

#Config
db_cred = dotenv_values("credentials/db-cred.env")

def main():
    with open("top_50_sg.json") as f:
        playlist = json.load(f)
    
    tracks = playlist["items"]
    track = tracks[0]
    pg_manager = db.PostgreManager(
        database = db_cred["database"],
        user = db_cred["user"],
        password = db_cred["password"],
        host = db_cred["host"],
        port = db_cred["port"]
        )
    conn = pg_manager.conn
    cursor = pg_manager.cursor
    cursor.execute("SELECT * FROM spotify.playlist.artists;")
    conn.commit()
    records = cursor.fetchall()
    print(records)
    conn.close()



if __name__ == "__main__":
    main()