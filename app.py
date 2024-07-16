from flask import Flask, render_template, jsonify
import threading
import time
import pyaudio
import numpy as np

app = Flask(__name__)

# Parameters for audio detection
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
THRESHOLD_DB = 115  # Approximate threshold for detecting sounds above 115 dB

# Variables to track shot times and detection flag
shot_times = []
min_time = float('inf')
max_time = 0
total_time = 0
shot_count = 0
shot_detected = False

# Lock for thread safety
lock = threading.Lock()

def detect_shot(audio_data):
    samples = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
    rms = np.sqrt(np.mean(samples**2))
    db = 20 * np.log10(rms) if rms > 0 else -np.inf
    
    if db > THRESHOLD_DB:
        return True
    return False

def listen_for_shots():
    global shot_times, min_time, max_time, total_time, shot_count, shot_detected
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
                    shot_detected = True
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

@app.route('/shot_detected')
def shot_detected_endpoint():
    global shot_detected
    with lock:
        detected = shot_detected
        shot_detected = False
        return jsonify({"shot_detected": detected})

if __name__ == '__main__':
    listener_thread = threading.Thread(target=listen_for_shots, daemon=True)
    listener_thread.start()
    app.run(host="0.0.0.0",port=3338,debug=True)
