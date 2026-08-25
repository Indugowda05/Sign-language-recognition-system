from function import *

from keras.models import model_from_json

import cv2
import numpy as np


# ============================================================
# LOAD MODEL
# ============================================================

with open("model.json", "r") as json_file:
    model_json = json_file.read()

model = model_from_json(model_json)
model.load_weights("model.h5")

print("Model loaded successfully!")


# ============================================================
# VARIABLES
# ============================================================

sequence = []
sentence = []
predictions = []

threshold = 0.80

# Predict every 3 frames instead of every frame
prediction_interval = 3

frame_counter = 0


# ============================================================
# CAMERA
# ============================================================

cap = cv2.VideoCapture(0)

# Lower camera resolution = faster processing
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# ============================================================
# MEDIAPIPE
# ============================================================

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:

    while cap.isOpened():

        # ----------------------------------------------------
        # READ CAMERA
        # ----------------------------------------------------

        ret, frame = cap.read()

        if not ret:
            break


        # ----------------------------------------------------
        # ROI
        # ----------------------------------------------------

        cropframe = frame[40:400, 0:300]

        cv2.rectangle(
            frame,
            (0, 40),
            (300, 400),
            (255, 255, 255),
            2
        )


        # ----------------------------------------------------
        # MEDIAPIPE DETECTION
        # ----------------------------------------------------

        image, results = mediapipe_detection(
            cropframe,
            hands
        )


        # ----------------------------------------------------
        # EXTRACT KEYPOINTS
        # ----------------------------------------------------

        keypoints = extract_keypoints(results)


        # ----------------------------------------------------
        # FAST SEQUENCE START
        # ----------------------------------------------------

        if results.multi_hand_landmarks:

            # If this is the first detected hand,
            # fill the 30-frame sequence immediately.
            if len(sequence) == 0:

                sequence = [keypoints.copy()] * sequence_length

            else:

                sequence.append(keypoints)

                sequence = sequence[-sequence_length:]


            frame_counter += 1


            # ------------------------------------------------
            # PREDICT ONLY EVERY FEW FRAMES
            # ------------------------------------------------

            if frame_counter % prediction_interval == 0:

                if len(sequence) == sequence_length:

                    res = model.predict(
                        np.expand_dims(sequence, axis=0),
                        verbose=0
                    )[0]

                    predicted_index = np.argmax(res)

                    predicted_action = actions[predicted_index]

                    confidence = res[predicted_index]


                    # ----------------------------------------
                    # SAVE PREDICTION
                    # ----------------------------------------

                    predictions.append(predicted_index)

                    predictions = predictions[-5:]


                    # ----------------------------------------
                    # STABLE PREDICTION
                    # ----------------------------------------

                    if len(predictions) >= 3:

                        recent = predictions[-3:]

                        if all(
                            prediction == predicted_index
                            for prediction in recent
                        ):

                            if confidence > threshold:

                                # Add only if different
                                # from previous word
                                if (
                                    len(sentence) == 0
                                    or predicted_action != sentence[-1]
                                ):

                                    sentence.append(
                                        predicted_action
                                    )


                    # Keep only latest result
                    if len(sentence) > 1:

                        sentence = sentence[-1:]


        else:

            # No hand detected
            sequence = []
            frame_counter = 0


        # ====================================================
        # OUTPUT BOX
        # ====================================================

        cv2.rectangle(
            frame,
            (0, 0),
            (500, 55),
            (245, 117, 16),
            -1
        )


        if len(sentence) > 0:

            output_text = "Output: " + sentence[-1]

        else:

            output_text = "Output: -"


        cv2.putText(
            frame,
            output_text,
            (10, 38),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )


        # ====================================================
        # DISPLAY
        # ====================================================

        cv2.imshow(
            "OpenCV Feed",
            frame
        )


        # ====================================================
        # QUIT
        # ====================================================

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# ============================================================
# RELEASE
# ============================================================

cap.release()
cv2.destroyAllWindows()