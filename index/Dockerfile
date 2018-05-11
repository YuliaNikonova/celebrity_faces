FROM ubuntu:latest

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

RUN apt-get install -y gcc-4.8
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 50


RUN apt-get install -y g++-4.8
RUN update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.8 50


RUN pip install Flask
RUN pip install annoy
RUN pip install jsonpickle
RUN pip install Cython==0.28.1
RUN pip install numpy


WORKDIR /index

COPY setup.py /index
#COPY python/*.py /index/python/
#COPY python/*.pyx /index/python/
#COPY python/*.pxd /index/python/
#COPY src/*.cpp /index/src/
#COPY src/*.h /index/src/
#COPY ut/*.py /index/ut/


#RUN python setup.py build_ext --inplace
#RUN python setup.py install



COPY run_in_container.sh /index
COPY index.py /index
COPY docker_config /index
COPY setup.py /index

COPY app/*.py /index/app/
COPY app/default_config /index/app

RUN chmod +x run_in_container.sh
CMD ["./run_in_container.sh"]