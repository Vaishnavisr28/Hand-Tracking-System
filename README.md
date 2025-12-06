# Hand Tracking & Virtual Boundary Interaction System :-

A Classical Computer-Vision Prototype for Real-Time Safety Zone Detection

This project implements a real-time hand tracking system that detects when a user’s hand approaches or touches a virtual object/boundary on the screen. The system runs fully on classical computer vision techniques — no MediaPipe, no OpenPose, no cloud AI APIs — and achieves ≥ 8 FPS on CPU-only execution.

The prototype demonstrates four interaction states:

=> NO_HAND → no hand detected in frame
=> SAFE → hand present but far from virtual object
=> WARNING → hand approaching object
=> DANGER → hand extremely close / touching object (triggers “DANGER DANGER”)
This fulfills the assignment requirement for a real-time safety interaction system using only traditional computer vision.

# Features:

1) Bare-hand detection (no color gloves required)

Uses hybrid HSV + YCrCb skin segmentation, plus face removal using classical Haar cascade.

2) Real-time performance (10–35 FPS on CPU)

Optimized for webcam input at 640×480 resolution.

3) Distance-based interaction model

The hand centroid is used to determine proximity to a virtual rectangular zone:
SAFE if comfortably far
WARNING if approaching
DANGER if touching or extremely close

4) Accurate DANGER detection
Uses:

Hand contour vs boundary intersection
Distance thresholding
Hysteresis to eliminate flicker

1. Visual overlays

The display shows:
- Virtual object (DANGER zone)
- Current interaction state
- Distance
- A large “DANGER DANGER” flashing overlay when triggered
- FPS counter

2. No deep learning models (optional Haar face detector only)

Fully compliant with assignment constraints:
- No MediaPipe
- No OpenPose
- No cloud APIs
- Pure OpenCV + NumPy

# System Architecture: 

┌───────────────────┐       ┌────────────────────┐       ┌──────────────────────┐
│  Webcam Feed      │       │  Skin Detection    │       │  Hand Extraction     │
│  (OpenCV)         ├──────>│  HSV + YCrCb mask  ├──────>|  Largest valid blob  │
└───────────────────┘       │  Face removal      │       │  Centroid + contour  │
                            └─────────┬──────────┘       └─────────┬────────────┘
                                      │                            │
                                      ▼                            ▼
                            ┌────────────────────┐        ┌────────────────────────┐
                            │Distance Computation│        │ Overlay Rendering      │
                            │ centroid→rectangle │        │ SAFE/WARNING/DANGER UI │
                            └─────────┬──────────┘        └─────────┬──────────────┘
                                      ▼                             ▼
                                   ┌──────────────────────────────────────────┐
                                   │       Classification Logic               │
                                   │  NO_HAND / SAFE / WARNING / DANGER       │
                                   └──────────────────────────────────────────┘

# Project Structure:

Hand-Tracking-System/
│
├── src/
│   ├── main.py                  
│   ├── hand_detector.py         
│   ├── interaction_logic.py     
│   ├── overlay.py               
│
├── README.md                   
└── requirements.txt             

# How it works: 

1. Skin Detection (HSV + YCrCb)

Two color spaces are combined using an AND operation.
This drastically reduces false positives from background walls, fabrics, etc.

2. Face Removal (for accuracy)

A classical Haar Cascade detects the user’s face, which is removed from the skin mask so it cannot be mistaken for a hand.

3. Hand Contour Selection

Among all skin blobs, the system selects the largest reasonable contour that fits typical hand size thresholds.

4. State Classification

The centroid of the hand contour is compared against:
Virtual rectangle
Distance thresholds
Result → NO_HAND, SAFE, WARNING, DANGER.

5. Visual Feedback

The system overlays:
Danger zone box
State indicator panel
Distance text
Red flashing “DANGER DANGER” banner

# How to run:

1. Install dependencies
pip install opencv-python numpy

2. Run the main file
python src/main.py

3. Controls

Press q or ESC → Quit the app

# Interaction States:-

State	Condition	UI Behavior
NO_HAND	No valid skin contour detected	Gray panel: "NO_HAND"
SAFE	Hand detected, distance ≥ WARNING threshold	Green panel: "SAFE"
WARNING	Distance < WARNING threshold (but > DANGER threshold)	Yellow panel: "WARNING"
DANGER	Distance < DANGER threshold or contour intersects box	Red panel + "DANGER DANGER" overlay

# Assignment Compliance

This system meets all requirements from the problem statement:

-> Real-time hand tracking
-> No MediaPipe, no OpenPose, no ML pose libraries
-> Uses classical vision: color segmentation, contours, HSV, YCrCb, Haar
-> Virtual object drawn on screen
-> Dynamic SAFE / WARNING / DANGER classification
-> “DANGER DANGER” warning on direct boundary contact
-> ≥ 8 FPS CPU-only
-> Clean UI & debug windows

# Future Improvements

Replace Haar with a better classical face detector (LBP)
Add depth estimation using stereo or monocular cues
Hand-shape validation using contour convexity
Adaptive skin-color calibration based on lighting

# Demo: 
https://drive.google.com/drive/u/0/folders/1BDTVkeNUhFdPxYn4Nv3g45rxc5haX8wZ

# Acknowledgments: 

This project was built using:

OpenCV for image processing
NumPy for numerical operations
Classical CV techniques for robust, real-time performance
