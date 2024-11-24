import time
import base64
import threading

import cv2
from cvzone.HandTrackingModule import HandDetector

import flet as ft

detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)


def capture_frame(image_control: str, page: ft.Page):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return None

    while True:
        success, frame = cap.read()
        if success:
            frame = cv2.flip(frame, flipCode=1)

            hands, frame = detector.findHands(frame)
            if hands:
                fingers1 = detector.fingersUp(hands[0])
                if len(hands) == 1:
                    cv2.putText(
                        img=frame,
                        text=str(sum(fingers1)),
                        org=(50, 50),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=(0, 0, 255),
                        thickness=2
                    )
                if len(hands) == 2:
                    fingers2 = detector.fingersUp(hands[1])
                    cv2.putText(
                        img=frame,
                        text=str(sum(fingers2) + sum(fingers1)),
                        org=(50, 50),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=(0, 0, 255),
                        thickness=2
                    )
            _, buffer = cv2.imencode(".jpg", frame)
            image_control.src_base64 = base64.b64encode(buffer).decode("utf-8")
            page.update()
        time.sleep(0.03)

def main(page: ft.Page):
    page.title = "Direct Camera Feed in Flet"
    page.padding = ft.padding.all(value=0)
    page.window.width = page.width
    page.window.height = page.height

    live_image = ft.Image(width=page.window.width, height=page.window.height, expand=True)

    threading.Thread(target=capture_frame, args=(live_image, page), daemon=True).start()

    page.add(live_image)

if __name__ == "__main__":
    ft.app(target=main)
