#!/usr/bin/env python3
import os
import subprocess

os.chdir('backend')
subprocess.run(['uv', 'run', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000', '--reload']) 