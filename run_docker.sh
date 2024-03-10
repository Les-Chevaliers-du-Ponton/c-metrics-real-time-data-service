docker build -t c-metrics-real-time-data-service .
docker run --name c-metrics-real-time --network=host -d c-metrics-real-time-data-service:latest