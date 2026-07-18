# Gesture Controlled Computer

This is a Python application that transforms your webcam into a touchless controller. By leveraging MediaPipe's precise hand tracking and OpenCV's real-time computer vision capabilities, the script translates human hand gestures into physical mouse movements, clicks, and scrolls on your operating system.

## Features

* **Cursor Movement:** Control the cursor smoothly by moving your index finger. Built-in linear interpolation (smoothing) prevents erratic cursor shaking.
* **Clicking & Dragging:** Pinch your thumb and index finger together to trigger a left-click. Hold the pinch to drag windows or select text across the screen.
* **Dynamic Scrolling:** Join your index and middle fingers together to activate scroll mode. The scrolling speed scales dynamically based on the velocity and acceleration of your hand movement.
* **Live FPS Counter:** Displays tracking performance directly on the camera feed window.

## Gesture Guide

* **Move Cursor:** Raise your index finger and move it around the frame.
* **Left-Click / Drag:** Bring your thumb and index finger within close proximity. Separate them to release.
* **Scroll Up/Down:** Keep your index and middle finger close together and move your hand vertically. The acceleration of your movement dictates the scroll speed.
