FROM tensorflow/tensorflow:1.7.0-py3


WORKDIR /nn_embeddings


COPY requirements.txt /nn_embeddings



RUN pip install Flask
RUN pip install scikit-learn==0.19.1
RUN pip install imageio
RUN pip install jsonpickle


COPY nn_embeddings.py /nn_embeddings
