import os
import cv2
from flask import Flask, request, send_from_directory, render_template
from beautify import beautify_image

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/beautify', methods=['POST'])
def beautify():
    image_file = request.files['image']
    image_path = os.path.join("uploads", image_file.filename)
    image_file.save(image_path)

    whitening = int(request.form['whitening'])
    blemish_removal = int(request.form['blemish_removal'])
    red_saturation = int(request.form['red_saturation'])

    image = cv2.imread(image_path)
    beautified_image = beautify_image(image, whitening=whitening, blemish_removal=blemish_removal,
                                      red_saturation=red_saturation)
    beautified_image_path = os.path.join("results", image_file.filename)
    cv2.imwrite(beautified_image_path, beautified_image)

    return send_from_directory("results", image_file.filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
