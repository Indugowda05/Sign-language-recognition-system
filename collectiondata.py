import os
import cv2

cap = cv2.VideoCapture(0)

directory = 'Image/'

# Create folders
actions = [
    'A', 'B', 'C', 'D',
    'F', 'G', 'H', 'I', 'J', 'K', 'L',
    'N', 'O', 'P', 'Q', 'R',
    'T', 'U', 'V', 'W', 'X', 'Y',
    'HELLO', 'YES', 'NO', 'LOVE', 'BYE'
]

for action in actions:
    os.makedirs(directory + action, exist_ok=True)

while True:

    _, frame = cap.read()

    count = {
        'a': len(os.listdir(directory + 'A')),
        'b': len(os.listdir(directory + 'B')),
        'c': len(os.listdir(directory + 'C')),
        'd': len(os.listdir(directory + 'D')),

        'f': len(os.listdir(directory + 'F')),
        'g': len(os.listdir(directory + 'G')),
        'h': len(os.listdir(directory + 'H')),
        'i': len(os.listdir(directory + 'I')),
        'j': len(os.listdir(directory + 'J')),
        'k': len(os.listdir(directory + 'K')),
        'l': len(os.listdir(directory + 'L')),

        'n': len(os.listdir(directory + 'N')),
        'o': len(os.listdir(directory + 'O')),
        'p': len(os.listdir(directory + 'P')),
        'q': len(os.listdir(directory + 'Q')),
        'r': len(os.listdir(directory + 'R')),

        't': len(os.listdir(directory + 'T')),
        'u': len(os.listdir(directory + 'U')),
        'v': len(os.listdir(directory + 'V')),
        'w': len(os.listdir(directory + 'W')),
        'x': len(os.listdir(directory + 'X')),
        'y': len(os.listdir(directory + 'Y')),

        'hello': len(os.listdir(directory + 'HELLO')),
        'yes': len(os.listdir(directory + 'YES')),
        'no': len(os.listdir(directory + 'NO')),
        'love': len(os.listdir(directory + 'LOVE')),
        'bye': len(os.listdir(directory + 'BYE'))
    }

    # Draw ROI
    cv2.rectangle(
        frame,
        (0, 40),
        (300, 400),
        (255, 255, 255),
        2
    )

    # Show camera
    cv2.imshow("data", frame)
    cv2.imshow("ROI", frame[40:400, 0:300])

    # Crop ROI
    frame = frame[40:400, 0:300]

    # Faster keyboard response
    interrupt = cv2.waitKey(1) & 0xFF

    # -------------------------
    # A - D
    # -------------------------

    if interrupt == ord('a'):
        cv2.imwrite(directory + 'A/' + str(count['a']) + '.png', frame)

    if interrupt == ord('b'):
        cv2.imwrite(directory + 'B/' + str(count['b']) + '.png', frame)

    if interrupt == ord('c'):
        cv2.imwrite(directory + 'C/' + str(count['c']) + '.png', frame)

    if interrupt == ord('d'):
        cv2.imwrite(directory + 'D/' + str(count['d']) + '.png', frame)

    # -------------------------
    # F - L
    # -------------------------

    if interrupt == ord('f'):
        cv2.imwrite(directory + 'F/' + str(count['f']) + '.png', frame)

    if interrupt == ord('g'):
        cv2.imwrite(directory + 'G/' + str(count['g']) + '.png', frame)

    if interrupt == ord('h'):
        cv2.imwrite(directory + 'H/' + str(count['h']) + '.png', frame)

    if interrupt == ord('i'):
        cv2.imwrite(directory + 'I/' + str(count['i']) + '.png', frame)

    if interrupt == ord('j'):
        cv2.imwrite(directory + 'J/' + str(count['j']) + '.png', frame)

    if interrupt == ord('k'):
        cv2.imwrite(directory + 'K/' + str(count['k']) + '.png', frame)

    if interrupt == ord('l'):
        cv2.imwrite(directory + 'L/' + str(count['l']) + '.png', frame)

    # -------------------------
    # N - R
    # -------------------------

    if interrupt == ord('n'):
        cv2.imwrite(directory + 'N/' + str(count['n']) + '.png', frame)

    if interrupt == ord('o'):
        cv2.imwrite(directory + 'O/' + str(count['o']) + '.png', frame)

    if interrupt == ord('p'):
        cv2.imwrite(directory + 'P/' + str(count['p']) + '.png', frame)

    if interrupt == ord('q'):
        cv2.imwrite(directory + 'Q/' + str(count['q']) + '.png', frame)

    if interrupt == ord('r'):
        cv2.imwrite(directory + 'R/' + str(count['r']) + '.png', frame)

    # -------------------------
    # T - Y
    # -------------------------

    if interrupt == ord('t'):
        cv2.imwrite(directory + 'T/' + str(count['t']) + '.png', frame)

    if interrupt == ord('u'):
        cv2.imwrite(directory + 'U/' + str(count['u']) + '.png', frame)

    if interrupt == ord('v'):
        cv2.imwrite(directory + 'V/' + str(count['v']) + '.png', frame)

    if interrupt == ord('w'):
        cv2.imwrite(directory + 'W/' + str(count['w']) + '.png', frame)

    if interrupt == ord('x'):
        cv2.imwrite(directory + 'X/' + str(count['x']) + '.png', frame)

    if interrupt == ord('y'):
        cv2.imwrite(directory + 'Y/' + str(count['y']) + '.png', frame)

    # -------------------------
    # WORDS
    # -------------------------

    # 1 = HELLO
    if interrupt == ord('1'):
        cv2.imwrite(
            directory + 'HELLO/' + str(count['hello']) + '.png',
            frame
        )

    # 2 = YES
    if interrupt == ord('2'):
        cv2.imwrite(
            directory + 'YES/' + str(count['yes']) + '.png',
            frame
        )

    # 3 = NO
    if interrupt == ord('3'):
        cv2.imwrite(
            directory + 'NO/' + str(count['no']) + '.png',
            frame
        )

    # 4 = LOVE
    if interrupt == ord('4'):
        cv2.imwrite(
            directory + 'LOVE/' + str(count['love']) + '.png',
            frame
        )

    # 5 = BYE
    if interrupt == ord('5'):
        cv2.imwrite(
            directory + 'BYE/' + str(count['bye']) + '.png',
            frame
        )

    # ESC = Exit
    if interrupt == 27:
        break

cap.release()
cv2.destroyAllWindows()