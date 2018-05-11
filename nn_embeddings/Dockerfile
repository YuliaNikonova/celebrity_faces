FROM tensorflow/tensorflow:1.7.0-py3


WORKDIR /nn_embeddings


ENV FACENET_SRC_DIR=/nn_embeddings/facenet_src
ENV MODEL_DIR=/nn_embeddings/data/models/20170512-110547
ENV PAIRS_PATH=/nn_embeddings/data/pairs.txt
ENV LFW_RAW_PATH=/nn_embeddings/data/lfw_raw


ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y libsm6 libxext6 libxrender-dev

RUN pip install Flask
RUN pip install scikit-learn==0.19.1
RUN pip install imageio
RUN pip install jsonpickle
RUN pip install opencv-python
RUN pip install tqdm


COPY nn_embeddings.py /nn_embeddings
COPY test_nn_lfw.py /nn_embeddings
COPY image_processing.py /nn_embeddings
COPY run.sh /nn_embeddings
COPY facenet_src /nn_embeddings/facenet_src/


RUN chmod +x run.sh
CMD ["./run.sh"]




