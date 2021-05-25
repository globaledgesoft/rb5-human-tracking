import cv2
import os
import numpy as np
from align import AlignDlib
import qcsnpe
import json
from create_embedding import create_embedding

img = True
thresh = 0.45
dlc = qcsnpe.qcsnpe("models/freez2.dlc",0)

def distance(emb1, emb2):
	return np.sum(np.square(emb1 - emb2))

def find_match(emb, test_emb):
	lowest_dist = None
	low_ind = None
	find = False
	for i, em in enumerate(emb):
		dist = distance(em, test_emb)
		if lowest_dist == None:
			lowest_dist = dist
			low_ind = i
		if dist < lowest_dist:
			lowest_dist = dist
			low_ind = i

	if lowest_dist > thresh:
		find = False
	else:
		find = True
		
	return lowest_dist, low_ind, find

def start_tracking(person):
	embedings = create_embedding(dlc, person)
	alignment = AlignDlib('models/shape_predictor_68_face_landmarks.dat')
	cam = cv2.VideoCapture(2)
	face_not_found = True 
	while face_not_found:
		ret, frame = cam.read()
		if not ret:
			print("failed to capture image")
			break
		rgb_img = frame[...,::-1].copy()
		img_width = frame.shape[0]

		# Detect face and return bounding box
		bb = alignment.getAllFaceBoundingBoxes(rgb_img)

		for i in range(len(bb)):
			x1, y1, w, h = bb[i].left(), bb[i].top(), bb[i].width(), bb[i].height()
			if x1 < 0:
				x1 = 0
			if y1 < 0:
				y1 = 0
			img_b = rgb_img[y1:y1+h, x1:x1+w]
			img_b = cv2.resize(img_b, (224,224))
			test_embed = dlc.predict(img_b)
			test_embed = test_embed/(np.sqrt(np.sum(np.square(test_embed))))
			dist, person_class, find = find_match(embedings, test_embed)
			print(dist,"=>", person_class)

			if find:
				face_not_found = False
				half_width = (bb[i].width())/(2)
				if ((bb[i].left() + half_width)/img_width > 0.5):
					pos = "right"
				else:
					pos = "left"
				payload = json.dumps({"name": person, "score": dist, "location": pos})
				return payload

