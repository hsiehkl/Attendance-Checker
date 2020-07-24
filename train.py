import face_recognition
# import dlib
from sklearn import svm
import os
import pickle


def train(model_name):

    # The training data would be all the face encodings from all the known images and the labels are their names
    encodings = []
    names = []

    # Training directory
    train_dir = os.listdir('train_dir')

    # Loop through each person in the training directory
    for person in train_dir:

        pix = os.listdir('train_dir/' + person)

        # Loop through each training image for the current person
        for person_img in pix:
            # Get the face encodings for the face in each image file
            face = face_recognition.load_image_file('train_dir/' + person + "/" + person_img)
            face_bounding_boxes = face_recognition.face_locations(face)

            #If training image contains exactly one face
            if len(face_bounding_boxes) == 1:
                face_enc = face_recognition.face_encodings(face)[0]
                # Add face encoding for current image with corresponding label (name) to the training data
                encodings.append(face_enc)
                names.append(person)
            else:
                print(person + "/" + person_img + " was skipped and can't be used for training")


    # Create and train the SVC classifier
    clf = svm.SVC(gamma='scale')
    clf.fit(encodings, names)

    # Save classifier
    pickle.dump(clf, open('models/' + '{}.pkl'.format(model_name), 'wb'))

