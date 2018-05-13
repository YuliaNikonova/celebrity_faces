FROM ubuntu:latest
ENV HOME /home


ENV INDEX_FILENAME /home/index/data/index_50.ann
ENV PATHS_JSON /home/index/data/paths_celeba_50000.json
ENV EMBEDDING_JSON /home/index/data/embedding_celeba_50000.json
ENV ACCURACY_TEST_DATA_PATH /home/index/data/test


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



COPY __init__.py setup.py $HOME/index/
COPY python/*.py python/*.pyx python/*.pxd $HOME/index/python/
COPY src/*.h src/*.cpp $HOME/index/src/
COPY ut/*.py $HOME/index/ut/

WORKDIR $HOME/index

# Install index
ENV LD_LIBRARY_PATH /usr/local/lib/python2.7/dist-packages/python
RUN python setup.py build_ext --inplace \
    && python setup.py install \
    && python -m unittest discover


COPY run.sh $HOME/index
COPY index.py $HOME/index
COPY setup.py $HOME/index
COPY nsw_index.py $HOME/index
COPY accuracy_test.py $HOME/index

RUN mkdir $HOME/index/test

RUN chmod +x run.sh
CMD ["./run.sh"]