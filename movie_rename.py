import os
import re
from tmdbv3api import TMDb, Movie

# Initialize TMDb and API key
tmdb = TMDb()
tmdb.api_key = 'your_tmdb_api_key'

# Initialize movie object
movie_db = Movie()

# Function to get the best match for a movie
def get_best_match(movie_name):
    try:
        search_results = movie_db.search(movie_name)
        if search_results:
            return search_results[0]
    except Exception as e:
        print(f"Error searching for {movie_name}: {e}")
    return None

# Function to sanitize folder names into a search query
def clean_folder_name(folder_name):
    # Replace dots, underscores, or dashes with spaces
    clean_name = re.sub(r'[._-]', ' ', folder_name)
    
    # Remove any trailing/leading spaces and numbers (like resolutions or years)
    clean_name = re.sub(r'\(\d{4}\)', '', clean_name)  # Remove (YYYY)
    clean_name = re.sub(r'\d{4}', '', clean_name)  # Remove standalone year
    clean_name = re.sub(r'\b\d+p\b', '', clean_name)  # Remove resolution like 720p, 1080p
    clean_name = re.sub(r'\b\d{3,4}\b', '', clean_name)  # Remove other numbers
    return clean_name.strip()

# Function to scan the directory for movies and rename
def scan_and_rename_folder(movie_folder_path):
    for folder in os.listdir(movie_folder_path):
        folder_path = os.path.join(movie_folder_path, folder)

        if os.path.isdir(folder_path):
            movie_name = clean_folder_name(folder)
            movie_data = get_best_match(movie_name)
            
            if movie_data:
                # Format: Movie Title (YYYY)
                new_folder_name = f"{movie_data.title} ({movie_data.release_date[:4]})"
                new_folder_path = os.path.join(movie_folder_path, new_folder_name)

                try:
                    # Rename the folder
                    os.rename(folder_path, new_folder_path)
                    print(f"Renamed: '{folder}' to '{new_folder_name}'")
                except Exception as e:
                    print(f"Error renaming '{folder}': {e}")
            else:
                print(f"No match found for '{folder}'")
        else:
            print(f"Skipping file: {folder}")

# Specify the path to the folder containing your movie directories
movie_folder_path = "/Volumes/EUROPE/TEST"

# Scan and rename movie folders
scan_and_rename_folder(movie_folder_path)
