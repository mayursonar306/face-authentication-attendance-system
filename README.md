# Face Authentication Attendance System

A real-time face recognition–based attendance system built using Python, MediaPipe, OpenCV, and Streamlit.  
The system allows employee face registration, real-time identification, and automatic attendance marking (Punch-In / Punch-Out) through a clean dashboard interface.

---

## Features

- Face registration using live webcam
- Real-time face recognition
- Automatic Punch-In and Punch-Out logic
- Duplicate entry prevention using cooldown
- Date-aware attendance tracking
- Enterprise-style dashboard UI
- Local database storage (SQLite)

---

## Tech Stack

- **Language:** Python  
- **Computer Vision:** OpenCV  
- **Face Detection:** MediaPipe FaceMesh  
- **Data Handling:** NumPy, Pandas  
- **Database:** SQLite  
- **UI Dashboard:** Streamlit  

---

## 📂 Project Structure

Face-Authentication-Attendance-System/
│
├── app.py # Streamlit dashboard (UI)
├── register_face.py # Face registration using webcam
├── recognize_face.py # Face recognition & attendance logic
├── database.py # SQLite database operations
├── utils.py # Encoding save/load utilities
│
├── database/
│ └── attendance.db # SQLite DB (generated at runtime)
│
├── encodings/ # Stored face encodings (generated)
│
├── requirements.txt
├── .gitignore
└── README.md


---

## ▶️ How to Run the Project

### 1. Execute all the commands

```bash
python -m venv face_env
face_env\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```
## Model and Approach Used

- MediaPipe FaceMesh is used for face detection and landmark extraction.
- Each detected face produces 468 facial landmarks, each with (x, y, z) coordinates.
- These landmarks are combined into a numerical feature vector.
- Face recognition is performed using Euclidean distance matching between live face vectors and stored encodings.
- A configurable distance threshold determines a valid match.
- No traditional neural network training is performed; instead, a feature-based matching approach is used for real-time efficiency.

## Training Process

- *There is no explicit ML training phase.
- *The registration process acts as training:

- The user stands in front of the camera.
- The system captures multiple face samples.
- Landmark-based feature vectors are extracted.
- These vectors are stored as reference encodings.
- This lightweight approach ensures fast execution and low system overhead.

## Accuracy Expectations

- High accuracy in controlled environments.
- Works best with:
   - Proper lighting
   - Frontal face orientation
   - Single person in frame
- Multiple samples during registration improve recognition consistency.

## Known Limitations

- Performance may degrade in very low-light conditions.
- Face masks, heavy occlusion, or extreme angles can affect detection.
- Basic spoof resistance only (no advanced liveness detection).
- Designed for single-face detection at a time.