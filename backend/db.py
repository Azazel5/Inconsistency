import os
import sqlite3
from datetime import datetime

# Define database file path in the workspace
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "inconsistency.db")

def get_connection():
    """Returns a connection to the SQLite database, creating the data directory if needed."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    """Initializes the database tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create playlists table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS playlists (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        channel_title TEXT,
        description TEXT,
        category TEXT,
        expected_retention TEXT,
        incentive_group TEXT, -- 'Aspirational' or 'Incentive'
        content_type TEXT,    -- 'Tutorial', 'Podcast', 'Book Summary', 'University Lectures', etc.
        fetched_at TEXT
    )
    """)
    
    # Create videos table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        id TEXT PRIMARY KEY,
        playlist_id TEXT NOT NULL,
        title TEXT NOT NULL,
        position INTEGER NOT NULL,
        duration_seconds INTEGER,
        view_count INTEGER NOT NULL,
        published_at TEXT,
        FOREIGN KEY (playlist_id) REFERENCES playlists (id) ON DELETE CASCADE
    )
    """)
    
    conn.commit()
    conn.close()

def save_playlist(playlist_meta, videos):
    """Saves or updates a playlist and its associated videos in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Save playlist metadata (INSERT OR REPLACE)
        cursor.execute("""
        INSERT OR REPLACE INTO playlists 
        (id, title, channel_title, description, category, expected_retention, incentive_group, content_type, fetched_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            playlist_meta["id"],
            playlist_meta["title"],
            playlist_meta.get("channel_title"),
            playlist_meta.get("description"),
            playlist_meta.get("category"),
            playlist_meta.get("expected_retention"),
            playlist_meta.get("incentive_group"),
            playlist_meta.get("content_type", "Tutorial"),
            playlist_meta.get("fetched_at", datetime.now().isoformat())
        ))
        
        # Remove existing videos for this playlist first to avoid duplicates or orphaned items
        cursor.execute("DELETE FROM videos WHERE playlist_id = ?", (playlist_meta["id"],))
        
        # Save new video list
        for video in videos:
            cursor.execute("""
            INSERT INTO videos 
            (id, playlist_id, title, position, duration_seconds, view_count, published_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                video["id"],
                playlist_meta["id"],
                video["title"],
                video["position"],
                video.get("duration_seconds", 0),
                video["view_count"],
                video.get("published_at")
            ))
            
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_playlists():
    """Retrieves all playlists from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM playlists ORDER BY category, title")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_playlist(playlist_id):
    """Retrieves metadata for a specific playlist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM playlists WHERE id = ?", (playlist_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_playlist_videos(playlist_id):
    """Retrieves all videos associated with a playlist, ordered by position."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videos WHERE playlist_id = ? ORDER BY position ASC", (playlist_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_playlist(playlist_id):
    """Deletes a playlist and all its associated videos."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM videos WHERE playlist_id = ?", (playlist_id,))
        cursor.execute("DELETE FROM playlists WHERE id = ?", (playlist_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
