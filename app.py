from flask import Flask, render_template, jsonify
import threading
import time
import pyaudio
import numpy as np
from scipy.signal import find_peaks

app = Flask(__name__)

# Parameters for audio detection
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
THRESHOLD = 1000

# Variables to track shot times
shot_times = []
min_time = float('inf')
max_time = 0
total_time = 0
shot_count = 0

# Lock for thread safety
lock = threading.Lock()

def detect_shot(audio_data):
    samples = np.frombuffer(audio_data, dtype=np.int16)
    peaks, _ = find_peaks(np.abs(samples), height=THRESHOLD)
    return len(peaks) > 0

def listen_for_shots():
    global shot_times, min_time, max_time, total_time, shot_count
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    while True:
        audio_data = stream.read(CHUNK)
        if detect_shot(audio_data):
            with lock:
                shot_time = time.time()
                shot_times.append(shot_time)
                if len(shot_times) > 1:
                    reaction_time = shot_times[-1] - shot_times[-2]
                    shot_count += 1
                    total_time += reaction_time
                    min_time = min(min_time, reaction_time)
                    max_time = max(max_time, reaction_time)
                    with open("shot_log.txt", "a") as log_file:
                        log_file.write(f"Shot {shot_count}: {reaction_time:.2f}s\n")
                    print(f"Shot detected! Reaction time: {reaction_time:.2f}s")

    stream.stop_stream()
    stream.close()
    p.terminate()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_stats')
def get_stats():
    with lock:
        if shot_count == 0:
            average_time = 0
        else:
            average_time = total_time / shot_count
        return jsonify({
            "min_time": min_time,
            "max_time": max_time,
            "average_time": average_time,
            "shot_count": shot_count
        })

if __name__ == '__main__':
    listener_thread = threading.Thread(target=listen_for_shots, daemon=True)
    listener_thread.start()
    app.run(host="0.0.0.0",port=3338, debug=True)