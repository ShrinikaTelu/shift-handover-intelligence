#!/bin/bash
cd /Users/shrinikatelu/shift-handover-project/backend
export PYTHONPATH=/Users/shrinikatelu/shift-handover-project/backend
python3 << 'EOF'
from main import app
import uvicorn
uvicorn.run(app, host='127.0.0.1', port=8000)
EOF
