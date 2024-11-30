import re

from . import COLLECTION_NAME, QDRANT_DB, MISTRAL_CLIENT, MODEL_NAME

def search_plants(query):
    # FILTRE Prix (à la "main")
    def get_price_filter(query):
        query = query.lower()
        if "cheap" in query or "not expensive" in query or "affordable" in query or "good price" in query or "small" in query or "price is less than" in query or "low-price" in query or "economical" in query:
            return lambda price: price < 8
        elif "expensive" in query or "costly" in query:
            return lambda price: 20 <= price <= 25
        return None

    def extract_price(document):
        match = re.search(r"priced at (\d+\.\d+) euros", document)
        return float(match.group(1)) if match else None

    # Génére l'embedding pour la requête
    query_embedding = MISTRAL_CLIENT.embeddings.create(model=MODEL_NAME, inputs=[query]).data[0].embedding

    # Recherche dans Qdrant
    results = QDRANT_DB.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=20,
    )

    # FILTRE Prix s'il y a (à la "main")
    price_filter = get_price_filter(query)
    if price_filter:
        filtered_results = []
        for result in results:
            document = result.payload["document"]
            price = extract_price(document)
            if price is not None and price_filter(price):
                filtered_results.append(result)
    else:
        filtered_results = results

    return filtered_results[:5] #Renvoie les 5 meilleurs results ici
