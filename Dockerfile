FROM python:3.9-slim-bullseye

RUN apt update && \
    apt install -y gcc git && \
    apt clean

# Install EPEL repository and necessary dependencies for Redis
RUN apt install -y wget tar && \
    wget http://download.redis.io/redis-stable.tar.gz && \
    tar xvzf redis-stable.tar.gz && \
    cd redis-stable && \
    make BUILD_TLS=yes && \
    apt remove -y wget tar && \
    apt autoremove -y

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir cython redis asyncpg && \
    pip install --no-cache-dir -r requirements.txt && \
    python3 setup.py build_ext --inplace

CMD ["/app/main.py"]
ENTRYPOINT ["python"]
