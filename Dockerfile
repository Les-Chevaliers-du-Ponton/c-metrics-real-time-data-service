FROM python:3.9-slim-bullseye

RUN apt update
RUN apt install gcc git -y

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir cython
RUN pip install --no-cache-dir redis
RUN pip install --no-cache-dir asyncpg
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 setup.py build_ext --inplace

CMD ["/app/main.py"]
ENTRYPOINT ["python"]