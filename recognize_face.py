import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime, timedelta

from utils import load_all_encodings
from database import init_db, mark_attendance, get_last_status


def match_face(face_vector, known_encodings, known_names, threshold=1.0):
    if not known_encodings:
        return None

    distances = [np.linalg.norm(face_vector - enc) for enc in known_encodings]
    best_match = int(np.argmin(distances))

    if distances[best_match] < threshold:
        return known_names[best_match]

    return None


def main():
    init_db()

    known_encodings, known_names = load_all_encodings()

    if not known_encodings:
        print("No registered faces found. Please register first.")
        return

    face_mesh = mp.solutions.face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=False
    )

    cap = cv2.VideoCapture(0)
    last_seen = {}

    print("Attendance camera started. Press ESC to stop.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb)

        if result.multi_face_landmarks:
            landmarks = result.multi_face_landmarks[0]

            vector = []
            for point in landmarks.landmark:
                vector.extend([point.x, point.y, point.z])

            face_vector = np.array(vector)
            name = match_face(face_vector, known_encodings, known_names)

            if name:
                now = datetime.now()

                if name not in last_seen or now - last_seen[name] > timedelta(minutes=2):
                    last_status = get_last_status(name)

                    if last_status is None:
                        mark_attendance(name, "Punch-In")
                        status = "Punch-In"

                    elif last_status == "Punch-In":
                        mark_attendance(name, "Punch-Out")
                        status = "Punch-Out"

                    else:
                        status = last_status

                    last_seen[name] = now
                else:
                    status = "Detected"

                cv2.putText(
                    frame,
                    f"{name} | {status}",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 255, 0),
                    2
                )

        cv2.imshow("Face Attendance System", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Attendance session ended")


if __name__ == "__main__":
    main()
