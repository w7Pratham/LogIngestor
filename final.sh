#!/bin/bash

docker compose up -d && \
docker exec app-1 /bin/bash -c """
    rm -rf /root/LogIngestor
    sleep 100s
    source /root/entrypoint.sh
"""

