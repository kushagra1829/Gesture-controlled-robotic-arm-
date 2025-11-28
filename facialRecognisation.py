from typing import List

import cv2
import mediapipe as mp
import serial
import time

# Initialize Mediapipe hand detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Establish serial connection to Arduino on COM3
ser = serial.Serial('COM3', 9600)  # Ensure the correct COM port is used
time.sleep(2)  # Wait for the serial connection to initialize

def get_finger_states(landmarks) -> List[int]:
    """
    Function to det`er9mine which fingers are up based on their landmark positions.
    A finger is considered up if the tip landmark y coordinate is smaller than the base landmark y coordinate.
    """
    finger_states: List[int] = []

    # Thumb detection: Check thumb's position relative to its base (landmarks 2 and 4)
    if landmarks[4].y < landmarks[2].y and abs(landmarks[4].x - landmarks[2].x) < 0.2:
        # Thumb up: Tip is higher than base and thumb is not too horizontal
        finger_states.append(1)  # Thumb up (1 means up)
    else:
        # Thumb down: Tip is lower than base or thumb is too horizontal
        finger_states.append(0)  # Thumb down (0 means down)

    # Index finger: Check if the tip (landmark 8) is higher than the base (landmark 6)
    if landmarks[8].y < landmarks[6].y:
        finger_states.append(1)  # Index up
    else:
        finger_states.append(0)  # Index down

    # Middle finger: Check if the tip (landmark 12) is higher than the base (landmark 10)
    if landmarks[12].y < landmarks[10].y:
        finger_states.append(1)  # Middle up
    else:
        finger_states.append(0)  # Middle down

    # Ring finger: Check if the tip (landmark 16) is higher than the base (landmark 14)
    if landmarks[16].y < landmarks[14].y:
        finger_states.append(1)  # Ring up
    else:
        finger_states.append(0)  # Ring down

    # Pinky finger: Check if the tip (landmark 20) is higher than the base (landmark 18)
    if landmarks[20].y < landmarks[18].y:
        finger_states.append(1)  # Pinky up
    else:
        finger_states.append(0)  # Pinky down

    return finger_states

cap=cv2.VideoCapture(0)
while True:
    # Read the frame from the camera
    success, img = cap.read()  # Capture frame from default camera
    if not success:
        print("Error: Failed to capture image.")
        break

    # Convert the BGR image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the frame for hand detection
    results = hands.process(img_rgb)

    # If hands are detected, draw landmarks and detect finger states
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on the image
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get finger states (up = 1, down = 0)
            finger_states = get_finger_states(hand_landmarks.landmark)

            # Format the finger states as a string that can be sent to Arduino
            # For example, '$01010' where 1 = up and 0 = down
            finger_string = '$' + ''.join(str(state) for state in finger_states)

            # Send the formatted finger states to Arduino over serial communication
            ser.write(finger_string.encode())  # Send data to Arduino

            # Optionally, print the state of each finger (0 = down, 1 = up) for debugging
            print(f"Fingers state (Thumb, Index, Middle, Ring, Pinky): {finger_states}")

            # Optionally, display text on the image indicating finger states
            finger_labels = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
            for i, state in enumerate(finger_states):
                text = f"{finger_labels[i]}: {'Up' if state == 1 else 'Down'}"
                cv2.putText(img, text, (10, 50 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame with hand detection
    cv2.imshow("Image", img)

    # Check for the 'Esc' key to break the loop (27 is the ASCII code for the Esc key)
    if cv2.waitKey(1) == 27:  # Wait for 1ms and check if 'Esc' key is pressed
        print("Exiting...")
        break

# Release the video capture object and close the window
cv2.VideoCapture(0).release()
cv2.destroyAllWindows()