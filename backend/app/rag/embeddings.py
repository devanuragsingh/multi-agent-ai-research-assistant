from sentence_transformers import SentenceTransformer

_model = None


def get_model():

    global _model

    if _model is None:

        print(
            "Loading embedding model..."
        )

        _model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return _model


def create_embeddings(
    chunks
):

    model = get_model()

    return model.encode(
        chunks,
        convert_to_numpy=True
    )


def create_query_embedding(
    query
):

    model = get_model()

    return model.encode(
        query,
        convert_to_numpy=True
    )