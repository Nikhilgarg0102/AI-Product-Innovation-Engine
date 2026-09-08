from sentence_transformers import SentenceTransformer
import os
import pickle


INPUT_FILE = "data/knowledge_base/company_knowledge.txt"
OUTPUT_FILE = "data/knowledge_base/embeddings.pkl"

MODEL_NAME = "all-MiniLM-L6-v2"


def load_knowledge():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    # Split knowledge into manageable chunks
    chunks = [
        chunk.strip()
        for chunk in text.split("\n\n")
        if chunk.strip()
    ]

    return chunks


def create_embeddings():

    print("EMBEDDING ENGINE")
    print("-" * 60)

    chunks = load_knowledge()

    print(f"Knowledge chunks: {len(chunks)}")

    print(f"Loading embedding model: {MODEL_NAME}")

    model = SentenceTransformer(MODEL_NAME)

    print("Creating embeddings...")

    embeddings = model.encode(
        chunks,
        show_progress_bar=True
    )

    print(f"Embedding shape: {embeddings.shape}")

    data = {
        "chunks": chunks,
        "embeddings": embeddings
    }

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "wb"
    ) as file:

        pickle.dump(
            data,
            file
        )

    print("\nEMBEDDING GENERATION COMPLETE")
    print("-" * 60)

    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    create_embeddings()