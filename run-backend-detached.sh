#!/bin/bash
cd /Users/shrinikatelu/shift-handover-project/backend
export PYTHONPATH=/Users/shrinikatelu/shift-handover-project/backend
nohup python3 << 'EOF' > /tmp/backend.log 2>&1 &
from main import app
import uvicorn
uvicorn.run(app, host='127.0.0.1', port=8000)
EOF
echo "Backend started (PID: $!)"
sleep 3
