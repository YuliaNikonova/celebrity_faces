FROM ubuntu:latest


RUN apt-get update \
  && apt-get install -y wget python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN pip install Flask
RUN pip install annoy
RUN pip install jsonpickle
RUN pip install Cython==0.28.1



RUN wget https://ftp.gnu.org/gnu/gcc/gcc-4.8.4/gcc-4.8.4.tar.gz
RUN tar xzf gcc-4.8.4.tar.gz

WORKDIR /gcc-4.8.4

RUN ./contrib/download_prerequisites

RUN mkdir objdir

WORKDIR /objdir

RUN ../gcc-4.8.4/configure --prefix=$HOME/gcc-4.8.4 --enable-languages=c,c++

#WORKDIR /index

#COPY run_in_container.sh /index
#COPY index.py /index
#COPY requirements.txt /index
#COPY docker_config /index
#COPY setup.py /index

#COPY app/*.py /index/app/
#COPY app/default_config /index/app
#COPY python/*.py /index/python/
#COPY python/*.pyx /index/python/
#COPY python/*.pxd /index/python/
#COPY src/*.cpp /index/src/
#COPY src/*.h /index/src/
#COPY ut/*.py /index/ut/


#RUN pip install Flask
#RUN pip install annoy
#RUN pip install jsonpickle
#RUN pip install Cython==0.28.1
#RUN chmod +x run_in_container.sh
#CMD ["./run_in_container.sh"]