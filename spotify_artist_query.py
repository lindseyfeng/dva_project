import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set your Spotify credentials
client_id = "bd0535c1e1bb4e7da4cae16ec39a464b"
client_secret = "22ee8ebd8b7448918a7c90c26f9072a2"

# Authenticate
auth_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret
)
sp = spotipy.Spotify(auth_manager=auth_manager)

cache = {}


# Function to get the artist's image
def get_artist_image(artist_name):
    if artist_name in cache:
        return cache[artist_name]
    results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
    if results["artists"]["items"]:
        artist = results["artists"]["items"][0]  # Get the first matching artist
        name = artist["name"]
        images = artist.get("images", [])
        if images:
            cache[artist_name] = images[0]["url"]
            return images[0]["url"]
        else:
            cache[artist_name] = None
            print(f"Artist: {name} has no image available.")
            return
    else:
        cache[artist_name] = None
        print(f"No artist found with the name {artist_name}.")
        return


# Example usage
artist_name = "Taylor Swift"  # Replace with the artist's name you want to search
print(artist_name, get_artist_image(artist_name))
