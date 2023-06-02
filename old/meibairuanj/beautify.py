import cv2
import dlib
import numpy as np


def beautify_image(image, ksize=5, sigma_color=75, sigma_space=75, whitening=0, blemish_removal=0, red_saturation=0):
    detector = dlib.get_frontal_face_detector()
    faces = detector(image, 1)

    if len(faces) > 0:
        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            roi = image[y:y+h, x:x+w]

            # 磨皮
            roi = cv2.bilateralFilter(roi, ksize, sigma_color, sigma_space)

            # 美白
            if whitening > 0:
                lab = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)
                l, a, b = cv2.split(lab)
                l = cv2.add(l, np.full_like(l, whitening, dtype=np.uint8))
                lab = cv2.merge([l, a, b])
                roi = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

            # 祛斑
            if blemish_removal > 0:
                gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
                kernel = np.ones((blemish_removal, blemish_removal), np.uint8)
                thresh = cv2.dilate(thresh, kernel, iterations=1)
                roi = cv2.inpaint(roi, thresh, blemish_removal, cv2.INPAINT_TELEA)

            # 纯红
            if red_saturation > 0:
                hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                h, s, v = cv2.split(hsv)
                s = cv2.add(s, np.uint8([red_saturation]))
                hsv = cv2.merge([h, s, v])
                roi = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

            image[y:y+h, x:x+w] = roi

    return image

