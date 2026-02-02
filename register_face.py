import cv2
import mediapipe as mp
import numpy as np
import time
import sys

from utils import save_encoding
from database import init_db, add_user


def main():
    init_db()

    if len(sys.argv) < 2:
        print("Name argument missing")
        return

    name = sys.argv[1]

    face_mesh = mp.solutions.face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=False
    )

    cap = cv2.VideoCapture(0)

    samples = []
    sample_count = 0
    last_capture = 0

    print(f"Starting face registration for: {name}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb)
        now = time.time()

        if result.multi_face_landmarks:
            landmarks = result.multi_face_landmarks[0]

            if now - last_capture >= 0.5:
                vector = []
                for point in landmarks.landmark:
                    vector.extend([point.x, point.y, point.z])

                samples.append(np.array(vector))
                sample_count += 1
                last_capture = now

                print(f"Sample collected: {sample_count}/20")

        cv2.putText(
            frame,
            f"User: {name}",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Samples: {sample_count}/20",
            (20, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow("Face Registration", frame)

        if sample_count >= 20:
            break

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    if samples:
        save_encoding(name, samples)
        add_user(name)
        print("Face registration completed successfully")
    else:
        print("Face registration failed")


if __name__ == "__main__":
    main()
