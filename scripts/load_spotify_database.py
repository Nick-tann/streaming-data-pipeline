import json
import psycopg2

def main():
    with open("top_50_sg.json") as f:
        playlist = json.load(f)
    
    tracks = playlist["items"]
    track = tracks[0]


if __name__ == "__main__":
    main()