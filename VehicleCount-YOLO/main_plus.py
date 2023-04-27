import cv2
import numpy as np
import time


def load_network(config_file, weights_file, class_file):
    net = cv2.dnn.readNetFromDarknet(config_file, weights_file)
    with open(class_file, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    return net, classes


def detect_objects(image, net, output_layers):
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(output_layers)
    return layer_outputs


def get_vehicle_boxes(layer_outputs, width, height, conf_threshold, nms_threshold):
    boxes = []
    confidences = []
    class_ids = []

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > conf_threshold:
                box = detection[0:4] * np.array([width, height, width, height])
                (centerX, centerY, w, h) = box.astype("int")

                x = int(centerX - (w / 2))
                y = int(centerY - (h / 2))

                boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    filtered_boxes = []
    for i in indices.flatten():
        if class_ids[i] in [2, 5, 7]:
            filtered_boxes.append(boxes[i])
    return filtered_boxes


def process_video(input_file, output_file, config_file, weights_file, class_file, conf_threshold=0.5,
                  nms_threshold=0.4):
    net, classes = load_network(config_file, weights_file, class_file)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

    cap = cv2.VideoCapture(input_file)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    vehicle_count = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        layer_outputs = detect_objects(frame, net, output_layers)
        vehicle_boxes = get_vehicle_boxes(layer_outputs, width, height, conf_threshold, nms_threshold)

        for box in vehicle_boxes:
            x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            vehicle_count += 1

        cv2.putText(frame, f"Vehicle count: {vehicle_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        out.write(frame)

    # 释放资源
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # 保存车辆总数到文件
    with open("vehicle_count.txt", "w") as f:
        f.write(f"Total vehicle count: {vehicle_count}")


if __name__ == "__main__":
    input_video = "input_video.mp4"
    output_video = "output_video.avi"
    config_file = "yolov4.cfg"
    weights_file = "yolov4.weights"
    class_file = "coco.names"

    process_video(input_video, output_video, config_file, weights_file, class_file)
