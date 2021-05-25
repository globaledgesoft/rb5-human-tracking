import flask
import werkzeug
import os
from utils_fun import check_person_exists, save_image, preprocess_image
import uuid

app = flask.Flask(__name__)

@app.route('/add_face', methods = ['GET', 'POST'])
def handle_request():
    imagefile = flask.request.files['image']
    img_bin = imagefile.read()
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    print("\nReceived image File name : " + imagefile.filename)
    name = os.path.splitext(filename)[0]
    if(check_person_exists(name, True)):
        img = preprocess_image(img_bin)
        save_image(img, name)
        # imagefile.save(os.path.join("people", name, str(uuid.uuid4()) + ".jpg"))
    return "Image Uploaded Successfully"

app.run(host="0.0.0.0", port=5000, debug=True)

