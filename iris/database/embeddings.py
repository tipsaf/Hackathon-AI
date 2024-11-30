# Embeddings par batch
def get_embeddings_by_chunks(data, chunk_size=50):
    from . import MISTRAL_CLIENT, MODEL_NAME

    chunks = [data[x : x + chunk_size] for x in range(0, len(data), chunk_size)]
    embeddings_response = [
        MISTRAL_CLIENT.embeddings.create(model=MODEL_NAME, inputs=c) for c in chunks
    ]
    return [d.embedding for e in embeddings_response for d in e.data]