FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN pip3 install mysqlclient

RUN pip3 install Pillow

COPY . /code
# COPY ./docker/dev/python/entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# ENTRYPOINT ["/entrypoint.sh"]

