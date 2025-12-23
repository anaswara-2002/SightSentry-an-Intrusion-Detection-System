# SightSentry-an-Intrusion-Detection-System

## Overview
This project is a Python-based academic application that performs face detection and basic image comparison using traditional computer vision techniques. The system uses OpenCV (cv2) with the Haar Cascade algorithm to detect faces from images and video streams. Sample celebrity images are used only for demonstration and learning purposes.

## Objectives
- To detect human faces from images and video using Haar Cascade
- To understand classical face detection techniques in OpenCV
- To perform basic image comparison on detected face regions
- To integrate face detection functionality with a simple Flask web interface

## Technologies Used
- Python
- OpenCV (cv2)
- Haar Cascade Classifier
- Flask
- HTML, CSS

## Algorithm Used
### Haar Cascade Classifier
Haar Cascade is a machine learning–based object detection algorithm that detects faces by using Haar-like features and a cascade of classifiers. It is efficient and suitable for real-time face detection but has limitations in accuracy under varying lighting and orientations.

## Project Structure
- main_video.py – Video-based face detection using OpenCV
- image_comparison.py – Compares detected face regions between images
- simple_facerec.py – Implements Haar Cascade–based face detection logic
- templates/ – HTML templates for the web interface
- static/ – Static files
- images/ – Sample images (celebrities) used for demonstration

## How It Works
1. Input images or video frames are captured and converted to grayscale.
2. Haar Cascade classifier detects face regions in the frame.
3. Detected faces are extracted and resized.
4. Basic image comparison techniques are applied to compare face regions.
5. The output is displayed through a Flask-based web interface.

## Setup Instructions
1. Clone the repository
2. Install required dependencies:
