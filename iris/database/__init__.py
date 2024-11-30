from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid
import pandas as pd


from mistralai import Mistral
from iris import MISTRAL_API_KEY

MISTRAL_CLIENT = Mistral(api_key=MISTRAL_API_KEY)
MODEL_NAME = "mistral-embed"

from iris import DATA_DIR

PLANT_DF = pd.read_csv(f"{DATA_DIR}/dataset.csv")

min_price = PLANT_DF['Price (eur)'].min()
max_price = PLANT_DF['Price (eur)'].max()

# Embedding
docs = [
    f"{row['Plant name']} is a plant described as {row['Description']}. "
    f"It requires {row['Light needs']} light, {row['Water needs']} water, and grows best in {row['Soil type']} soil. "
    f"It is priced at {row['Price (eur)']} euros (plants in this dataset range between {min_price} and {max_price} euros) "
    f"and has a rating of {row['Rating (out of 5)']} out of 5. "
    for _, row in PLANT_DF.iterrows()
]


from .embeddings import get_embeddings_by_chunks
# Generation embeddings pour les descriptions de plantes
embeddings = get_embeddings_by_chunks(docs, chunk_size=50)


# Initialiser Qdrant Client
QDRANT_DB = QdrantClient(path=f"{DATA_DIR}/qdrant_database")
COLLECTION_NAME = "plants_embeddings"

# Créer une collection Qdrant
QDRANT_DB.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
)

# Insérer les embeddings dans la base de données Qdrant
QDRANT_DB.upsert(
    collection_name=COLLECTION_NAME,
    points=[
        PointStruct(
            id=str(uuid.uuid4()),  # unique UUID pour chaque point
            vector=embeddings[i],  # Embedding généré
            payload={"document": docs[i]},
        )
        for i in range(len(docs))
    ],
)

from .search import search_plants
from .similar_search import find_similar_plants


def test():
    def display_rag_results(results: list):
        print("\nSearch Results:")
        if not results:
            print("No plants match your specific criteria.")
        else:
            for result in results:
                print(result.payload["document"])

    user_query = "I want a cheap indoor plant."
    results = search_plants(user_query)
    display_rag_results(results)