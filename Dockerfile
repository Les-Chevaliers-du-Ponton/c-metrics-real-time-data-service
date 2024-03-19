FROM python:3.10-slim-bullseye

RUN apt update
RUN apt install gcc git -y
RUN apt-get install g++ -y

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir cython
RUN pip install --no-cache-dir redis
RUN pip install --no-cache-dir asyncpg
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 setup.py build_ext --inplace

WORKDIR /app
COPY . /app

CMD ["/app/main.py"]
ENTRYPOINT ["python"]