Gesture-Controlled Serial Communication (Arduino & Python)
This project utilizes computer vision to detect hand gestures and sends the state of each finger (up or down) via serial communication to an Arduino board. This allows for controlling physical components (like a robotic hand, servo motors, or LEDs) using simple hand movements captured by a webcam.
Features
Real-time Hand Detection: Uses Google's MediaPipe library for accurate, single-hand tracking.
Finger State Recognition: Determines if the thumb, index, middle, ring, and pinky fingers are up or down.
Serial Communication: Transmits finger states to an Arduino board over a specified COM port (default COM3).
OpenCV Integration: Displays a live video feed with overlaid landmarks and finger status text for debugging.
Prerequisites
Before running the code, you need to have Python installed, along with several libraries.
Python Libraries
Install the required Python packages using pip:
pip install opencv-python mediapipe pyserial
Hardware Requirements
A computer with a webcam.
An Arduino board (e.g., Arduino Uno, Nano) connected via USB.
Hardware components connected to the Arduino (e.g., LEDs, servos) configured to receive serial data.
Usage
1. Arduino Setup
You must configure your Arduino to listen for serial data on the baud rate 9600. The Python script sends a formatted string in the format $[T][I][M][R][P] (e.g., $01010 where 1 is up, 0 is down).
You will need an Arduino sketch to read this input from the serial port and act upon it.
2. Python Script Configuration
Open the Python script (your_script_name.py) and modify the serial port connection line if you are not using Windows COM3:
# Establish serial connection to Arduino
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to 'dev/ttyUSB0' or 'dev/tty.usbmodem...' for Linux/Mac
3. Running the Program
Execute the Python script from your terminal:
python your_script_name.py
A window named "Image" will open, displaying your webcam feed. When a hand is detected, the finger states will be printed to the console and sent to the Arduino. Press the Esc key to exit the application.
Troubleshooting
serial.SerialException: ... The system cannot find the file specified: The COM port specified (COM3 in the example) is incorrect or the Arduino is not plugged in. Check your device manager/system settings for the correct port name.
Hand not detected: Ensure adequate lighting and hold your hand clearly in front of the camera. The script is configured for a single hand only (max_num_hands=1).
ModuleNotFoundError: Make sure you installed all required libraries using pip install opencv-python mediapipe pyserial.
Contributing
Feel free to fork this repository, open issues, and submit pull requests.
License
This project is open-source and available under the MIT License.





