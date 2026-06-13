import json
import os
import urllib.parse
from http.server import SimpleHTTPRequestHandler, HTTPServer
from backend.db import get_playlists, get_playlist, get_playlist_videos, save_playlist, delete_playlist
from backend.analyzer import analyze_playlist_data, aggregate_comparisons
from backend.fetcher import fetch_playlist_details

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

class APIRouterHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Initialize SimpleHTTPRequestHandler to serve files from FRONTEND_DIR
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def end_headers(self):
        # Add CORS headers for developer ease-of-use
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        # Route API requests
        if path == "/api/playlists":
            self.handle_get_playlists()
        elif path.startswith("/api/playlists/"):
            # Format: /api/playlists/<id>
            playlist_id = path.split("/")[-1]
            self.handle_get_playlist_details(playlist_id)
        elif path == "/api/comparisons":
            self.handle_get_comparisons()
        else:
            # Fallback to serving static files from the frontend folder
            super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        if path == "/api/playlists/add":
            self.handle_add_playlist()
        elif path.startswith("/api/playlists/delete/"):
            playlist_id = path.split("/")[-1]
            self.handle_delete_playlist(playlist_id)
        else:
            self.send_json_error("API endpoint not found", 404)

    # API Request Handlers
    
    def handle_get_playlists(self):
        """Returns metadata and metrics for all playlists (excluding detailed video lists)."""
        try:
            playlists = get_playlists()
            analyzed_playlists = []
            
            for p in playlists:
                videos = get_playlist_videos(p["id"])
                analysis = analyze_playlist_data(p, videos)
                # Remove detailed video list to reduce response size
                analysis.pop("videos", None)
                analyzed_playlists.append(analysis)
                
            self.send_json_response(analyzed_playlists)
        except Exception as e:
            self.send_json_error(f"Error loading playlists: {str(e)}")

    def handle_get_playlist_details(self, playlist_id):
        """Returns full video stats and curves for a single playlist."""
        try:
            p = get_playlist(playlist_id)
            if not p:
                self.send_json_error(f"Playlist with ID '{playlist_id}' not found.", 404)
                return
                
            videos = get_playlist_videos(playlist_id)
            analysis = analyze_playlist_data(p, videos)
            self.send_json_response(analysis)
        except Exception as e:
            self.send_json_error(f"Error loading playlist details: {str(e)}")

    def handle_get_comparisons(self):
        """Returns averaged retention curves aggregated by categories, groups, and content types."""
        try:
            playlists = get_playlists()
            analyzed_playlists = []
            
            for p in playlists:
                videos = get_playlist_videos(p["id"])
                analysis = analyze_playlist_data(p, videos)
                analyzed_playlists.append(analysis)
                
            comparisons = aggregate_comparisons(analyzed_playlists)
            self.send_json_response(comparisons)
        except Exception as e:
            self.send_json_error(f"Error calculating comparisons: {str(e)}")

    def handle_add_playlist(self):
        """Fetches a new playlist via YouTube API and saves it to the database."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data.decode('utf-8'))
            
            url_or_id = body.get("url_or_id", "").strip()
            category = body.get("category", "Programming").strip()
            expected_retention = body.get("expected_retention", "Medium").strip()
            incentive_group = body.get("incentive_group", "Aspirational").strip()
            content_type = body.get("content_type", "Tutorial").strip()
            
            if not url_or_id:
                self.send_json_error("Playlist URL or ID is required.", 400)
                return
                
            # Parse playlist ID if a full URL is provided
            playlist_id = url_or_id
            if "youtube.com" in url_or_id or "youtu.be" in url_or_id:
                parsed = urllib.parse.urlparse(url_or_id)
                query = urllib.parse.parse_qs(parsed.query)
                if "list" in query:
                    playlist_id = query["list"][0]
                else:
                    self.send_json_error("Could not parse Playlist ID from the provided URL. Ensure it contains 'list=...'.", 400)
                    return
            
            # Fetch live playlist details from YouTube Data API
            playlist_meta, videos = fetch_playlist_details(playlist_id)
            
            # Enrich metadata with the user's categories/incentive groups
            playlist_meta["category"] = category
            playlist_meta["expected_retention"] = expected_retention
            playlist_meta["incentive_group"] = incentive_group
            playlist_meta["content_type"] = content_type
            
            # Save to SQLite
            save_playlist(playlist_meta, videos)
            
            # Recalculate and return details
            analysis = analyze_playlist_data(playlist_meta, videos)
            self.send_json_response(analysis)
            
        except ValueError as ve:
            self.send_json_error(str(ve), 400)
        except Exception as e:
            self.send_json_error(f"Failed to fetch and analyze playlist: {str(e)}", 500)

    def handle_delete_playlist(self, playlist_id):
        """Deletes a playlist and its associated videos from the database."""
        try:
            p = get_playlist(playlist_id)
            if not p:
                self.send_json_error("Playlist not found.", 404)
                return
                
            delete_playlist(playlist_id)
            self.send_json_response({"success": True, "message": f"Deleted playlist {playlist_id} successfully."})
        except Exception as e:
            self.send_json_error(f"Failed to delete playlist: {str(e)}")

    # JSON helper functions
    
    def send_json_response(self, data, status=200):
        response_bytes = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(response_bytes))
        self.end_headers()
        self.wfile.write(response_bytes)

    def send_json_error(self, message, status=500):
        self.send_json_response({"error": message}, status)

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIRouterHandler)
    print(f"Server running on port {port}... Open http://localhost:{port} in your browser.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        httpd.server_close()
