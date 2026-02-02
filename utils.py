import pickle
import os

ENCODING_DIR = "encodings"

def save_encoding(name, encodings):
    path = os.path.join(ENCODING_DIR, f"{name}.pkl")

    with open(path, "wb") as f:
        pickle.dump(encodings, f)


def load_all_encodings():
    all_encodings = []
    names = []

    for file in os.listdir(ENCODING_DIR):
        if file.endswith(".pkl"):
            name = file.split(".")[0]

            with open(os.path.join(ENCODING_DIR, file), "rb") as f:
                enc = pickle.load(f)

                for e in enc:
                    all_encodings.append(e)
                    names.append(name)

    return all_encodings, names
