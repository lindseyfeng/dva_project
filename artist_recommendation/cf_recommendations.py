import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix, vstack
from lightfm import LightFM


class ArtistRecommender:
    def __init__(self, artist_cluster_path, spotify_data_path):
        """
        Initializes the recommender with data paths.

        Parameters:
        artist_cluster_path (str): Path to the artist cluster CSV file.
        spotify_data_path (str): Path to the Spotify dataset CSV file.
        """
        self.artist_cluster_path = artist_cluster_path
        self.spotify_data_path = spotify_data_path
        self.artist_cluster_df = self._load_csv(
            artist_cluster_path, skip_bad_lines=True
        )
        self.spotify_data_df = self._load_csv(spotify_data_path, skip_bad_lines=True)

    @staticmethod
    def _load_csv(path, skip_bad_lines=False):
        """Loads a CSV file into a pandas DataFrame."""
        if skip_bad_lines:
            return pd.read_csv(path, on_bad_lines="skip")
        return pd.read_csv(path)

    def get_cluster_id_for_artist(self, artist_name):
        """
        Gets the cluster ID for a given artist name.

        Parameters:
        artist_name (str): The artist name to search for.

        Returns:
        str or int: Cluster ID or a message indicating the artist was not found.
        """
        df = self.artist_cluster_df
        df["artists"] = df["artists"].fillna("")
        cluster_info = df[
            df["artists"].str.contains(artist_name, case=False, regex=False)
        ]
        return (
            cluster_info["cluster"].iloc[0]
            if not cluster_info.empty
            else "Artist not found"
        )

    def get_artists_in_cluster(self, cluster_id):
        """
        Gets a list of artists belonging to a specific cluster.

        Parameters:
        cluster_id (int): The cluster ID to filter artists by.

        Returns:
        list: A list of artists in the specified cluster.
        """
        df = self.artist_cluster_df
        artists_in_cluster = df[df["cluster"] == cluster_id]["artists"]
        return artists_in_cluster.tolist()

    def get_filtered_artist_data(self, artist_list):
        """
        Filters the Spotify data for a list of artists.

        Parameters:
        artist_list (list): List of artist names to filter by.

        Returns:
        pd.DataFrame: Filtered Spotify dataset.
        """
        return self.spotify_data_df[
            self.spotify_data_df[' "artistname"'].isin(artist_list)
        ]

    def create_interaction_matrix(self, filtered_artist_df):
        """
        Creates a user-item interaction matrix from filtered artist data.

        Parameters:
        filtered_artist_df (pd.DataFrame): Filtered artist data.

        Returns:
        pd.DataFrame: Crosstab of user interactions with artists.
        """
        return pd.crosstab(
            filtered_artist_df["user_id"], filtered_artist_df[' "artistname"']
        )

    def collect_user_feedback(self, artist_names, max_artists=10):
        """
        Collects feedback from the user for a list of artists.

        Parameters:
        artist_names (list): List of artist names to collect feedback on.
        max_artists (int): Maximum number of artists to ask about.

        Returns:
        np.ndarray: Binary interaction vector for the user.
        """
        interactions = np.zeros(len(artist_names))
        print("Enter 'y' if you like the artist, or 'n' if you dislike them.")

        accepted_artists_count = 0
        for artist in artist_names:
            if accepted_artists_count >= max_artists:
                break
            artist_index = artist_names.index(artist)
            interactions[artist_index] = 1
            accepted_artists_count += 1
        return interactions

    def recommend_artists(
        self, interaction_matrix, new_user_interactions, artist_names, top_n=5
    ):
        """
        Recommends top artists for the user based on interaction matrix.

        Parameters:
        interaction_matrix (csr_matrix): Existing user-item interaction matrix.
        new_user_interactions (np.ndarray): Interaction vector for the new user.
        artist_names (list): List of artist names in the dataset.
        top_n (int): Number of recommendations to return.

        Returns:
        list: Top N recommended artists.
        """
        new_user_sparse = csr_matrix(new_user_interactions)
        updated_interactions = vstack([interaction_matrix, new_user_sparse])

        model = LightFM(loss="warp")
        model.fit(updated_interactions, epochs=10, num_threads=4)

        new_user_id = updated_interactions.shape[0] - 1
        scores = model.predict(new_user_id, np.arange(len(artist_names)))
        recommended_indices = np.argsort(scores)[-top_n:][::-1]
        return [artist_names[i] for i in recommended_indices]


def main():
    artist_cluster_path = "artist_clusters.csv"
    spotify_data_path = "spotify_dataset.csv"

    recommender = ArtistRecommender(artist_cluster_path, spotify_data_path)
    favorite_artist = input("Enter your favorite artist: ")

    cluster_id = recommender.get_cluster_id_for_artist(favorite_artist)
    if cluster_id == "Artist not found":
        print("Sorry, artist not found.")
        return

    # find similar artists that were grouped into the same cluster in preprocessing
    similar_artists = recommender.get_artists_in_cluster(cluster_id)
    if not similar_artists:
        print("No artists found in the cluster.")
        return

    # matrix completion part
    filtered_artist_df = recommender.get_filtered_artist_data(similar_artists)
    cross_df = recommender.create_interaction_matrix(filtered_artist_df)

    artist_names = cross_df.columns.tolist()
    new_user_interactions = recommender.collect_user_feedback(artist_names)

    recommendations = recommender.recommend_artists(
        csr_matrix(cross_df.values), new_user_interactions, artist_names
    )

    print("Top recommended artists for you:")
    for artist in recommendations:
        print(artist)


if __name__ == "__main__":
    main()
