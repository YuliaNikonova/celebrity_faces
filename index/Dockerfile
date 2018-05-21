FROM ubuntu:latest
ENV HOME /home


ENV INDEX_FILENAME $HOME/index_service/data/index_celeba.ann
ENV NSW_INDEX_FILENAME $HOME/index_service/data/index_celeba_nsw
ENV PATHS_JSON $HOME/index_service/data/paths_celeba.json
ENV EMBEDDING_JSON $HOME/index_service/data/embeddings_celeba.json
ENV ACCURACY_TEST_DATA_PATH $HOME/index_service/data/test
ENV TEST_CASES_FILENAME $HOME/index_service/data/index_celeba_test_cases.json


RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    build-essential \
    ca-certificates \
    gcc \
    gcc-4.8 \
    git \
    libhdf5-dev \
    libpq-dev \
    make \
    python-pip \
    python2.7 \
    python2.7-dev \
    ssh \
    vim \
    wget \
    && apt-get autoremove \
    && apt-get clean

RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 50


RUN pip install \
    annoy \
    Cython==0.28.1 \
    Flask \
    h5py==2.8.0rc1 \
    jsonpickle \
    nose \
    numpy \
    unittest2 \
    tqdm


COPY __init__.py accuracy_test.py index_service_flask.py nsw_index.py setup.py create_nsw_index.py $HOME/index_service/
COPY python/*.py python/*.pyx python/*.pxd $HOME/index_service/python/
COPY src/*.h src/*.cpp $HOME/index_service/src/
COPY ut/*.py $HOME/index_service/ut/
RUN mkdir $HOME/index_service/test

WORKDIR $HOME/index_service


# Install index
ENV LD_LIBRARY_PATH /usr/local/lib/python2.7/dist-packages/python
RUN python setup.py build_ext --inplace \
    && python setup.py install \
    && python -m unittest discover


CMD ["python", "index_service_flask.py"]
