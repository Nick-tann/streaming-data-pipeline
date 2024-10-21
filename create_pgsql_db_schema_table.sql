
-- Playlist details table
DROP TABLE IF EXISTS spotify.playlist.playlist_details;
CREATE TABLE spotify.playlist.playlist_details (
    track_id VARCHAR(25),
    added_at TIMESTAMP
);

-- tracks table
DROP TABLE IF EXISTS spotify.playlist.tracks;
CREATE TABLE spotify.playlist.tracks (
    track_id VARCHAR(25),
    album_id VARCHAR(25),
    album_type VARCHAR(25),
    name VARCHAR(100),
    popularity SMALLINT,
    is_local BOOLEAN,
    disc_number SMALLINT,
    track_number SMALLINT,
    duration_ms SMALLINT,
    explicit BOOLEAN
);

-- Playlist details table
DROP TABLE IF EXISTS spotify.playlist.albums;
CREATE TABLE spotify.playlist.albums (
    album_id VARCHAR(25),
    album_type VARCHAR(25),
    name VARCHAR(100),
    release_date DATE
);

-- Playlist details table
DROP TABLE IF EXISTS spotify.playlist.artists;
CREATE TABLE spotify.playlist.artists (
    track_id VARCHAR(25),
    artist_id VARCHAR(25),
    name VARCHAR(100)
);