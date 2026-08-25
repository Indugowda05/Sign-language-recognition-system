from function import *
from time import sleep
import os
import cv2


# Create folders for each action and sequence
for action in actions:
    for sequence in range(no_sequences):
        try:
            os.makedirs(
                os.path.join(DATA_PATH, action, str(sequence))
            )
        except:
            pass


# Set MediaPipe model
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:

    # Loop through actions
    for action in actions:

        # Loop through sequences
        for sequence in range(no_sequences):

            # IMPORTANT:
            # One image = one sequence
            image_path = os.path.join(
                'Image',
                action,
                str(sequence) + '.png'
            )

            frame = cv2.imread(image_path)

            # Check image
            if frame is None:
                print("ERROR: Image not found:", image_path)
                continue

            # Loop through 30 frames
            for frame_num in range(sequence_length):

                # Make detections
                image, results = mediapipe_detection(
                    frame,
                    hands
                )

                # Draw landmarks
                draw_styled_landmarks(
                    image,
                    results
                )

                # Display information
                if frame_num == 0:

                    cv2.putText(
                        image,
                        'STARTING COLLECTION',
                        (120, 200),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        4,
                        cv2.LINE_AA
                    )

                    cv2.putText(
                        image,
                        'Collecting frames for {} Video Number {}'.format(
                            action,
                            sequence
                        ),
                        (15, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 255),
                        1,
                        cv2.LINE_AA
                    )

                    cv2.imshow(
                        'OpenCV Feed',
                        image
                    )

                    cv2.waitKey(200)

                else:

                    cv2.putText(
                        image,
                        'Collecting frames for {} Video Number {}'.format(
                            action,
                            sequence
                        ),
                        (15, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 255),
                        1,
                        cv2.LINE_AA
                    )

                    cv2.imshow(
                        'OpenCV Feed',
                        image
                    )

                # Extract keypoints
                keypoints = extract_keypoints(results)

                # Save keypoints
                npy_path = os.path.join(
                    DATA_PATH,
                    action,
                    str(sequence),
                    str(frame_num)
                )

                np.save(
                    npy_path,
                    keypoints
                )

                # Press Q to stop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    exit()


cv2.destroyAllWindows()

print("MP_Data created successfully!")