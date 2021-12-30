import cv2
import numpy as np
from sklearn.decomposition import PCA
from PIL import Image
from math import sqrt
import pickle
import os

def preprocess_img(user_id, num_imgs=3):
    # n x l x w c
    # take user ID and retrieve the photos of the user
    path = os.path.join(os.getcwd(), 'static', 'userPhotos')
    userPhotos = [Image.open(
        os.path.join(path,f'user-{user_id}-photo-{i}.jpg')) for i in range(num_imgs)]
    userPhotos2 = [np.asarray(userPhotos[i]) for i in range(num_imgs)]
    userPhotos = np.array(userPhotos2)
    print(userPhotos.shape)
    return userPhotos


def authUserPhoto(photosDB, photoTaken):

    threshold = 5  # han7adedo lesa

    images = photosDB

    n, img_height, img_width, n_channels = images.shape  # el n fel awel wala el a5er

    resize1 = 100
    resize2 = 100
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    X_train = np.zeros((n, resize1, resize2))
    X_test = np.zeros((resize1, resize2))

    for i in range(n):
        img = images[i, :, :, :]

        img = 0.2989 * img[:, :, 0] + 0.5870 * \
            img[:, :, 1] + 0.1140 * img[:, :, 2]
        img = np.array(img, dtype='uint8')
        faces = face_cascade.detectMultiScale(
            img, scaleFactor=1.05, minNeighbors=5)
        img = img[faces[0][1]:faces[0][1]+faces[0]
                  [3], faces[0][0]:faces[0][0]+faces[0][2]]
        img = cv2.resize(img, (100, 100))
        X_train[i, :, :] = img

    img = photoTaken
    img = 0.2989 * img[:, :, 0] + 0.5870 * img[:, :, 1] + 0.1140 * img[:, :, 2]
    img = np.array(img, dtype='uint8')
    faces = face_cascade.detectMultiScale(
        img, scaleFactor=1.05, minNeighbors=5)
    img = img[faces[0][1]:faces[0][1]+faces[0]
              [3], faces[0][0]:faces[0][0]+faces[0][2]]
    X_test = cv2.resize(img, (100, 100))

    X_train = X_train.reshape(
        (X_train.shape[0], X_train.shape[1]*X_train.shape[2]))
    X_test = X_test.reshape((1, X_test.shape[0]*X_test.shape[1]))
    filename = "D:\\Work\\MyWork\\Internships\\STP\\Combined-Project\\cpd\\Door-Security-system-interface\\Backend\\finalized_model.sav"
    pca = pickle.load(open(filename, 'rb'))

    X_train_pca = pca.transform(X_train)
    X_test_pca = pca.transform(X_test)

    dist = []
    for i in range(X_train_pca.shape[0]):
        dist.append(sqrt(np.sum((X_train_pca[i, :]-X_test_pca)**2)))

    distance = min(dist)

    if distance < threshold:
        return 1
    else:
        return 0
