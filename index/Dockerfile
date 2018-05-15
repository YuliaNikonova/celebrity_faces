FROM ubuntu:latest
ENV HOME /home


ENV INDEX_FILENAME /home/index_service/data/index_celeba.ann
ENV PATHS_JSON /home/index_service/data/paths_celeba.json
ENV EMBEDDING_JSON /home/index_service/data/embeddings_celeba.json
ENV ACCURACY_TEST_DATA_PATH /home/index_service/data/test


RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    build-essential \
    ca-certificates \
    gcc \
    git \
    wget \
    libpq-dev \
    make \
    python-pip \
    python2.7 \
    python2.7-dev \
    ssh \
    && apt-get autoremove \
    && apt-get clean




RUN apt-get install -y gcc-4.8 vim
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 50


RUN apt-get install -y libhdf5-dev
RUN pip install \
    Flask \
    annoy \
    jsonpickle \
    Cython==0.28.1 \
    numpy \
    nose \
    unittest2 \
    h5py==2.8.0rc1



COPY __init__.py setup.py $HOME/index_service/
COPY python/*.py python/*.pyx python/*.pxd $HOME/index_service/python/
COPY src/*.h src/*.cpp $HOME/index_service/src/
COPY ut/*.py $HOME/index_service/ut/

WORKDIR $HOME/index_service

# Install index
ENV LD_LIBRARY_PATH /usr/local/lib/python2.7/dist-packages/python
RUN python setup.py build_ext --inplace \
    && python setup.py install \
    && python -m unittest discover


COPY index_service_flask.py $HOME/index_service
COPY setup.py $HOME/index_service
COPY nsw_index.py $HOME/index_service
COPY accuracy_test.py $HOME/index_service

RUN mkdir $HOME/index_service/test

#RUN py
CMD ["python", "index_service_flask.py"]