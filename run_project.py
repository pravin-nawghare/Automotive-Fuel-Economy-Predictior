import subprocess
import sys
import time

print("Starting FastAPI server...")
fastapi_process = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--reload"]
)

time.sleep(3)

print("Starting Streamlit UI...")
streamlit_process = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "app.py"]
)

try:
    fastapi_process.wait()
    streamlit_process.wait()
except KeyboardInterrupt:
    fastapi_process.terminate()
    streamlit_process.terminate()