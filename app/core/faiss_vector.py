import faiss
import numpy as np
from app.core.logger import logger

class FaissVector:
    def __init__(self, dim=512, index_file="faiss_index.bin"):
        self.dim = dim
        self.index_file = index_file
        self.index = faiss.IndexFlatL2(self.dim)
        self.load_index()

    def load_index(self):
        try:
            self.index = faiss.read_index(self.index_file)
        except Exception as e:
            print(f"Index file not found or failed to load. Creating a new index. Error: {e}")
            self.index = faiss.IndexFlatL2(self.dim)

    def save_index(self):
        try:
            faiss.write_index(self.index, self.index_file)
        except Exception as e:
            print(f"Error saving index: {e}")

    def add(self, embeddings):
        embeddings = np.array(embeddings).astype('float32')
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)
        if embeddings.shape[1] != self.dim:
            raise ValueError(f"Embedding dimension {embeddings.shape[1]} does not match index dimension {self.dim}")
        self.index.add(embeddings)
        self.save_index()

    def search(self, embedding, k=10, threshold=0.8):
        if not isinstance(embedding, np.ndarray):
            embedding = np.array(embedding, dtype='float32')
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)

        distances, indices = self.index.search(embedding, self.index.ntotal)

        filtered_distances = []
        filtered_indices = []

        for distance, index in zip(distances[0], indices[0]):
            if distance < threshold:
                filtered_distances.append(distance)
                filtered_indices.append(index)
                if len(filtered_distances) >= k:
                    break

        return np.array(filtered_distances), np.array(filtered_indices)