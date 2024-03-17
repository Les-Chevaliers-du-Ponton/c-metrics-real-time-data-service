docker build -t c-metrics-real-time-data-service .
docker run --name c-metrics-real-time -d c-metrics-real-time-data-service:latest
# add -it for debugging

# docker stop c-metrics-real-time
# docker start c-metrics-real-time