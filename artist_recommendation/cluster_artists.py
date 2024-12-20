import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


class ArtistClustering:
    def __init__(self, data_path, k):
        self.data_path = data_path
        self.k = k
        self.raw_data = self.read_data(self.data_path)
        self.artist_features = self.get_artist_data()
        self.artist_clusters = None
    

    def read_data(self, data_path):
        df = pd.read_csv(data_path)
        return df


    def get_artist_data(self):
        self.raw_data['artists'] = self.raw_data['artists'].str.split(';')
        self.raw_data = self.raw_data.explode('artists').reset_index(drop=True)
        artist_features = self.raw_data.groupby('artists').agg({
                        'danceability': 'mean',
                        'energy': 'mean',
                        'key': 'mean',
                        'loudness': 'mean',
                        'mode': 'mean',
                        'speechiness': 'mean',
                        'acousticness': 'mean',
                        'instrumentalness': 'mean',
                        'liveness': 'mean',
                        'valence': 'mean',
                        'tempo': 'mean'
                    }).reset_index()
        # print(len(artist_features['artists'].unique()))
        return artist_features


    
    def create_clusters(self):
        features = self.artist_features.iloc[:, 1:]
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        kmeans = KMeans(n_clusters=self.k, random_state=24)
        self.artist_clusters = self.artist_features.copy()
        self.artist_clusters['cluster'] = kmeans.fit_predict(features_scaled)
        self.artist_clusters = self.artist_clusters[['artists', 'cluster']]
        self.artist_clusters.sort_values(by=['cluster'], inplace=True)
    

    def write_artist_clusters(self):
        self.artist_clusters.to_csv('./artist_clusters.csv', index=False)
    

    def create_artist_clusters(self):
        self.create_clusters()
        self.write_artist_clusters()

