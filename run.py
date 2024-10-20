import subprocess
import time

def run_flask():
    print("Starting Flask backend...")
    flask_process = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)  
    return flask_process

def run_streamlit():
    print("Starting Streamlit frontend...")
    streamlit_process = subprocess.Popen(["streamlit", "run", "streamlit_app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return streamlit_process

if __name__ == "__main__":
    flask_process = run_flask()

    streamlit_process = run_streamlit()

    try:
        flask_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("Terminating both processes...")
        flask_process.terminate()
        streamlit_process.terminate()
