FROM ubuntu:latest
ENV HOME /home

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

RUN pip install \
    Flask \
    annoy \
    jsonpickle \
    Cython==0.28.1 \
    numpy

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

#WORKDIR /index

#COPY run_in_container.sh /index
#COPY index.py /index
#COPY requirements.txt /index
#COPY docker_config /index
#COPY setup.py /index

#COPY app/*.py /index/app/
#COPY app/default_config /index/app

#RUN chmod +x run_in_container.sh
#CMD ["./run_in_container.sh"]