import os
import cv2
import uuid
import numpy as np

def check_person_exists(name, create=True):
    if os.path.isdir(os.path.join("people",name)):
        print("Person already exists")
        return True
    else:
        if create:
            os.mkdir(os.path.join("people", name))
            print("New person directory added")
            return True
        else:
            print("Person doesn't exist in the database")
            return False

def preprocess_image(img):
    npimg = np.fromstring(img, np.uint8)
    # convert numpy array to image
    img = cv2.imdecode(npimg, cv2.IMREAD_ANYCOLOR)
    img = cv2.resize(img, (250,250))
    return img

def save_image(img, name):
    print("saving img at: ", os.path.join("people", name, str(uuid.uuid4()) + ".jpg"))
    cv2.imwrite(os.path.join("people", name, str(uuid.uuid4()) + ".jpg"), img)
    return