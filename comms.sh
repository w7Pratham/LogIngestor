#!/bin/bash

exec python3 /root/LogIngestor/app.py &
exec python3 /root/LogIngestor/app1.py &
exec python3 /root/LogIngestor/app2.py &
echo ">>> Three are exectued <<<"
