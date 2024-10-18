
-- Playlist details table
DROP TABLE IF EXISTS spotify.playlist.playlist_details;
CREATE TABLE spotify.playlist.playlist_details (
    track_id VARCHAR(25),
    added_at TIMESTAMP
);