FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

#ENV PYTHONPATH="${PYTHONPATH}:/code/src"

#EXPOSE 8000:8000

CMD ["python3", "src/__main__.py"]
