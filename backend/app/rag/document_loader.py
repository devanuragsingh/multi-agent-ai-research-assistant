def load_document(path):
    with open(path, "rb") as f:
        return f.read()
