FROM python:3.5-alpine

WORKDIR /website

COPY run.sh /website
COPY requirements.txt /website
COPY website.py /website


COPY app/*.py /website/app/
COPY app/templates/*.html /website/app/templates/

RUN mkdir /website/app/static/
RUN mkdir /website/app/static/uploaded_images

RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN chmod +x run.sh
CMD ["./run.sh"]
