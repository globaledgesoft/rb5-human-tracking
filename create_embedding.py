import numpy as np
import os.path
import cv2
from align import AlignDlib

alignment = AlignDlib('models/shape_predictor_68_face_landmarks.dat')

class IdentityMetadata():
	def __init__(self, base, name, file):
		# dataset base directory
		self.base = base
		# identity name
		self.name = name
		# image file name
		self.file = file

	def __repr__(self):
		return self.image_path()

	def image_path(self):
		return os.path.join(self.base, self.name, self.file) 
	
def load_metadata(person):
	metadata = []
	for f in sorted(os.listdir(os.path.join("people", person))):
		# Check file extension. Allow only jpg/jpeg' files.
		ext = os.path.splitext(f)[1]
		if ext == '.jpg' or ext == '.jpeg':
			metadata.append(IdentityMetadata("people", person, f))
	return np.array(metadata)

def load_image(path):
	img = cv2.imread(path, 1)
	return img[...,::-1]

def distance(emb1, emb2):
	return np.sum(np.square(emb1 - emb2))

def align_image(img):
	return alignment.align(224, img, alignment.getLargestFaceBoundingBox(img), 
						landmarkIndices=AlignDlib.OUTER_EYES_AND_NOSE)

def unalign_image(img):
	bb = alignment.getLargestFaceBoundingBox(img)
	print(bb)
	
	x1, y1, w, h = bb.left(), bb.top(), bb.width(), bb.height()
	img_b = img[y1:y1+h, x1:x1+w]
	img_b = cv2.resize(img_b, (224,224))
	return img_b
	
def get_array_size(array):
		return array.ndim and array.size
			
def create_embedding(dlc, person):
	print("creating metadata")	
	metadata = load_metadata(person)

	# Initialize the OpenFace face alignment utility
	alignment = AlignDlib('models/shape_predictor_68_face_landmarks.dat')
	embedded = np.zeros((metadata.shape[0], 2622))
	for i, m in enumerate(metadata):
		img = load_image(m.image_path())
		img = align_image(img)
		img = np.array((img))
		if get_array_size(img) == 0:
			print("failed to detect face, thus ignoring the image")
			continue
		img = (img / 255.).astype(np.float32)
		# obtain embedding vector for image
		embedded[i] = dlc.predict(img)

	return embedded





