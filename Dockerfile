FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install git+https://github.com/e183b796621afbf902067460/defi-head-core.git#egg=defi-head-core

COPY ./src /code/src

CMD ["python3", "src/__main__.py"]
