from annoy import AnnoyIndex
import numpy as np

INDEX_FILENAME = 'data/index.ann'
PATHS_NPY = 'data/paths.npy'
EMBEDDING_NPY = 'data/embeddings.npy'


def build_index(embeddings):
    dim = embeddings.shape[1]
    u = AnnoyIndex(dim)
    try:
        u.load(INDEX_FILENAME)
        print("Index loaded")
    except FileNotFoundError:
        print('Building index...')
        for index, vector in enumerate(embeddings):
            if index % 500 == 0:
                print("{} vectors added".format(index))
            u.add_item(index, vector)
            u.build(10)  # 10 trees
            u.save(INDEX_FILENAME)

            u = AnnoyIndex(dim)
            u.load(INDEX_FILENAME)
    return u


def main():
    embeddings = np.load(EMBEDDING_NPY)
    index = build_index(embeddings)


if __name__ == "__main__":
    # execute only if run as a script
    main()
