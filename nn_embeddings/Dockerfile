FROM tensorflow/tensorflow:1.2.0-py3


WORKDIR /nn_embeddings


COPY requirements.txt /nn_embeddings



RUN pip install -r requirements.txt


COPY nn_embeddings.py /nn_embeddings
