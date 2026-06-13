import os
import sys
import threading
import time
import webbrowser

# Ensure the project root is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from backend.db import DB_PATH
from backend.seed import seed_database
from backend.server import run_server

def open_browser(port):
    """Waits for a second for the server to spin up, then opens the user's browser."""
    time.sleep(1.0)
    url = f"http://localhost:{port}"
    print(f"Automatically launching browser to {url}...")
    webbrowser.open(url)

def main():
    # 1. Load environment variables
    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        print("No .env file found. Running with default configurations and demonstration datasets.")
        
    port = int(os.getenv("PORT", 8000))
    
    # 2. Check if database needs seeding
    # If the database file doesn't exist or is empty, we automatically seed it.
    if not os.path.exists(DB_PATH) or os.path.getsize(DB_PATH) == 0:
        print("Database not found or empty. Seeding standard demonstration datasets...")
        try:
            seed_database()
        except Exception as e:
            print(f"WARNING: Error while seeding database: {e}")
    else:
        print(f"Found existing database at: {DB_PATH}")
        
    # 3. Open the browser in a separate thread
    browser_thread = threading.Thread(target=open_browser, args=(port,))
    browser_thread.daemon = True
    browser_thread.start()
    
    # 4. Start the web server
    run_server(port)

if __name__ == "__main__":
    main()
