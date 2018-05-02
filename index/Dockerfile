FROM python:3.5-alpine


RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk --no-cache --update-cache add gcc gfortran python python-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

WORKDIR /index

COPY run_in_container.sh /index
COPY index.py /index
COPY requirements.txt /index
COPY docker_config /index/

COPY app/*.py /index/app/
COPY app/default_config /index/app

RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["chmod +x", "run_in_container.sh"]
CMD ["./run_in_container.s"]