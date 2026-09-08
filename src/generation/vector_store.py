import faiss
import pickle
import numpy as np
import os


EMBEDDINGS_FILE = "data/knowledge_base/embeddings.pkl"
INDEX_FILE = "data/knowledge_base/knowledge.index"


def build_vector_store():

    print("FAISS VECTOR STORE")
    print("-" * 60)

    # Load embeddings
    with open(
        EMBEDDINGS_FILE,
        "rb"
    ) as file:

        data = pickle.load(file)

    embeddings = np.asarray(
        data["embeddings"],
        dtype="float32"
    )

    print(f"Vectors loaded: {len(embeddings)}")
    print(f"Vector dimensions: {embeddings.shape[1]}")

    # Create FAISS index
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    # Add vectors
    index.add(embeddings)

    print(f"Vectors indexed: {index.ntotal}")

    # Save index
    os.makedirs(
        os.path.dirname(INDEX_FILE),
        exist_ok=True
    )

    faiss.write_index(
        index,
        INDEX_FILE
    )

    print("\nVECTOR STORE CREATED")
    print("-" * 60)

    print(f"Saved to: {INDEX_FILE}")


if __name__ == "__main__":
    build_vector_store()