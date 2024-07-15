# virtual-target-training



brew install portaudio

pip install pyaudio


# Dryfire Training Application

This application is designed to help you train your airsoft shooting skills by displaying targets on a screen and measuring the reaction times from when a target appears until a shot is detected.

## Features
- Displays a new target on the screen every 10 seconds.
- Measures and records the shooter's reaction time.
- Tracks statistics such as the fastest, slowest, and average reaction times.
- Logs all shots and reaction times in a log file (`shot_log.txt`).
- Real-time display of statistics on the web interface.

## Installation

Follow these steps to install and run the application on your local machine:

1. **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4. **Install the required packages:**
    For Mac also install:
    ```bash
    brew install portaudio
    ```
    Python packages:
    ```bash
    pip install -r requirements.txt
    ```


5. **Start the application:**
    ```bash
    python app.py
    ```

6. **Open the web interface:**
    Open your web browser and go to `http://127.0.0.1:3338/`, or the http://<deviceIp>:3338/.

## Usage

1. Once the application is running, you will see the homepage with the title "Dryfire Training" and a timer counting down to the next target.
2. Each target will remain visible for 5 seconds and then disappear.
3. While the targets are appearing, the application listens for shot sounds using your computer's microphone.
4. The reaction time from when a target appears until a shot is detected is measured and recorded.
5. The statistics are updated every second and displayed on the web interface.

## Log File

Each time a shot is detected, the reaction time is logged in `shot_log.txt` in the root of the project.

## Requirements

- Python 3.6 or higher
- Flask
- pyaudio
- numpy
- scipy

## Important Files

- `app.py`: Main file of the Flask application.
- `templates/index.html`: HTML template for the web interface.
- `static/app.js`: JavaScript file responsible for displaying targets and updating the timer.
- `requirements.txt`: Contains all required Python packages.

## Authors

This application was developed by mvleest-code.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.
