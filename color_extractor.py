import numpy as np
from sklearn.cluster import KMeans
from PIL import Image


def load_image(uploaded_file):
    """Load uploaded image and convert to RGB numpy array."""
    image = Image.open(uploaded_file).convert("RGB")
    return np.array(image)


def preprocess_image(image, size=(150, 150)):
    """Resize image to speed up K-Means clustering."""
    img = Image.fromarray(image)
    img = img.resize(size, Image.LANCZOS)
    return np.array(img)


def extract_colors(image, n_colors=5):
    """Run K-Means clustering to extract dominant colors."""
    small_img = preprocess_image(image)

    # Reshape: (H, W, 3) → (H*W, 3) — each row is one pixel
    pixels = small_img.reshape(-1, 3).astype(float)

    # Run K-Means AI
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)

    # Get dominant colors as integers
    colors = kmeans.cluster_centers_.astype(int)

    # Calculate percentage of image each color covers
    labels = kmeans.labels_
    counts = np.bincount(labels)
    percentages = (counts / counts.sum() * 100).round(1)

    # Sort by percentage — largest first
    sorted_idx = np.argsort(percentages)[::-1]
    colors = colors[sorted_idx]
    percentages = percentages[sorted_idx]

    return colors, percentages