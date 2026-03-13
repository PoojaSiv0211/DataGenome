import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


def prepare_numeric_features(df):
    numeric_df = df.select_dtypes(include=[np.number]).copy()
    numeric_df = numeric_df.dropna()
    return numeric_df


def compute_correlation(numeric_df):
    return numeric_df.corr()


def build_3d_feature_embedding(numeric_df):

    scaler = StandardScaler()
    scaled = scaler.fit_transform(numeric_df)

    feature_matrix = scaled.T

    n_components = 3 if feature_matrix.shape[0] >= 3 else 2

    pca = PCA(n_components=n_components, random_state=42)
    coords = pca.fit_transform(feature_matrix)

    if n_components == 2:
        coords = np.column_stack([coords, np.zeros(len(coords))])

    features = numeric_df.columns.tolist()

    return pd.DataFrame({
        "feature": features,
        "x": coords[:,0],
        "y": coords[:,1],
        "z": coords[:,2]
    })


def cluster_features(embedding_df):

    n_features = len(embedding_df)
    n_clusters = min(3, n_features)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)

    embedding_df = embedding_df.copy()
    embedding_df["cluster"] = kmeans.fit_predict(
        embedding_df[["x","y","z"]]
    )

    cluster_map = {}

    for cluster_id in sorted(embedding_df["cluster"].unique()):

        cluster_map[int(cluster_id)] = embedding_df.loc[
            embedding_df["cluster"] == cluster_id, "feature"
        ].tolist()

    return embedding_df, cluster_map


def strongest_relationships(corr, top_n=5):

    pairs = []
    cols = list(corr.columns)

    for i in range(len(cols)):
        for j in range(i+1, len(cols)):
            pairs.append((cols[i], cols[j], corr.iloc[i,j]))

    pairs = sorted(pairs, key=lambda x: abs(x[2]), reverse=True)

    return pairs[:top_n]

def generate_dataset_report(df, numeric_df, corr):

    rows, cols = df.shape
    num_numeric = numeric_df.shape[1]

    relationships = strongest_relationships(corr)

    report = f"""
This dataset contains {rows} rows and {cols} columns.

It includes {num_numeric} numeric features used for analysis.

The system analyzes relationships between features using correlation analysis.

Strong relationships discovered include:
"""

    for f1,f2,value in relationships:
        direction = "positive" if value > 0 else "negative"
        report += f"\n• {f1} and {f2} show a {direction} relationship ({value:.2f})"

    report += "\n\nFeatures are then embedded into a 3D space using PCA to visualize the structural similarity of dataset variables."

    return report