import os
import re
import requests
from datetime import datetime

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"

def parse_iso8601_duration(duration_str):
    """
    Parses an ISO 8601 duration string (e.g., 'PT1H23M45S', 'PT45S', 'PT1H3S') 
    into total duration in seconds.
    """
    if not duration_str:
        return 0
    # Pattern to capture Hours, Minutes, and Seconds
    pattern = re.compile(r'P(?:(?P<days>\d+)D)?T?(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?')
    match = pattern.match(duration_str)
    if not match:
        return 0
    
    parts = match.groupdict()
    days = int(parts['days']) if parts['days'] else 0
    hours = int(parts['hours']) if parts['hours'] else 0
    minutes = int(parts['minutes']) if parts['minutes'] else 0
    seconds = int(parts['seconds']) if parts['seconds'] else 0
    
    return days * 86400 + hours * 3600 + minutes * 60 + seconds

def get_api_key():
    """Retrieves the YouTube API key from environment variables."""
    return os.getenv("YOUTUBE_API_KEY")

def fetch_playlist_details(playlist_id):
    """
    Queries YouTube API for playlist metadata and all its video statistics.
    Returns:
        tuple: (playlist_metadata_dict, list_of_videos_dict)
    """
    api_key = get_api_key()
    if not api_key or "YOUR_YOUTUBE_API_KEY" in api_key:
        raise ValueError("YouTube API key is missing or not configured in your environment/dotenv file.")
    
    # 1. Fetch Playlist Metadata
    playlist_url = f"{YOUTUBE_API_URL}/playlists"
    params = {
        "part": "snippet",
        "id": playlist_id,
        "key": api_key
    }
    response = requests.get(playlist_url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch playlist metadata: {response.text}")
    
    playlist_data = response.json()
    if not playlist_data.get("items"):
        raise Exception(f"No playlist found with ID: {playlist_id}")
    
    snippet = playlist_data["items"][0]["snippet"]
    playlist_meta = {
        "id": playlist_id,
        "title": snippet.get("title", "Unknown Playlist"),
        "channel_title": snippet.get("channelTitle", "Unknown Channel"),
        "description": snippet.get("description", ""),
        "fetched_at": datetime.now().isoformat()
    }
    
    # 2. Fetch Playlist Items (all videos in the playlist)
    items_url = f"{YOUTUBE_API_URL}/playlistItems"
    videos_meta_list = []
    page_token = None
    position = 0
    
    while True:
        params = {
            "part": "snippet,contentDetails",
            "playlistId": playlist_id,
            "maxResults": 50,
            "key": api_key
        }
        if page_token:
            params["pageToken"] = page_token
            
        res = requests.get(items_url, params=params)
        if res.status_code != 200:
            raise Exception(f"Failed to fetch playlist items: {res.text}")
            
        data = res.json()
        items = data.get("items", [])
        
        for item in items:
            video_id = item["contentDetails"].get("videoId")
            video_title = item["snippet"].get("title", "Deleted Video")
            published_at = item["contentDetails"].get("videoPublishedAt") or item["snippet"].get("publishedAt")
            
            # Avoid adding private or deleted videos that have no video ID
            if video_id:
                videos_meta_list.append({
                    "id": video_id,
                    "title": video_title,
                    "position": position,
                    "published_at": published_at
                })
                position += 1
                
        page_token = data.get("nextPageToken")
        if not page_token:
            break
            
    if not videos_meta_list:
        return playlist_meta, []
        
    # 3. Fetch Video Details (view count & duration) in batches of 50
    video_details = {}
    video_url = f"{YOUTUBE_API_URL}/videos"
    
    for i in range(0, len(videos_meta_list), 50):
        batch = videos_meta_list[i:i+50]
        batch_ids = [v["id"] for v in batch]
        
        params = {
            "part": "statistics,contentDetails",
            "id": ",".join(batch_ids),
            "key": api_key
        }
        res = requests.get(video_url, params=params)
        if res.status_code != 200:
            raise Exception(f"Failed to fetch video statistics: {res.text}")
            
        data = res.json()
        items = data.get("items", [])
        
        for item in items:
            v_id = item["id"]
            stats = item.get("statistics", {})
            content = item.get("contentDetails", {})
            
            # Convert views to integer (default to 0 if not found/disabled)
            view_count = int(stats.get("viewCount", 0))
            duration_iso = content.get("duration", "")
            duration_seconds = parse_iso8601_duration(duration_iso)
            
            video_details[v_id] = {
                "view_count": view_count,
                "duration_seconds": duration_seconds
            }
            
    # 4. Merge details back into video list
    final_videos = []
    for v in videos_meta_list:
        details = video_details.get(v["id"], {"view_count": 0, "duration_seconds": 0})
        v["view_count"] = details["view_count"]
        v["duration_seconds"] = details["duration_seconds"]
        
        # Include only videos that are accessible (i.e. view count is greater than 0, or keep it 0 but mark it)
        # Note: Some newly uploaded videos or private videos might have 0 views, but we keep them.
        final_videos.append(v)
        
    return playlist_meta, final_videos
