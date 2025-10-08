import os
import cv2
from face_recognition.api import face_detector
from model import User
import numpy as np
import face_recognition
import os
import speech_recognition as sr

def load_faces_in_db():
    # Delete all images in the "images" directory
    image_directory = "images"
    for filename in os.listdir(image_directory):
        file_path = os.path.join(image_directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    users = User.query.all()
    face_images = []
    number_of_times_to_upsample = 1  # Define the value for upsampling

    for user in users:
        if user.face:
            # Convert the binary string to a numpy array
            image_data = np.frombuffer(user.face, np.uint8)
            img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

            # Save the image to the "images" directory
            image_path = os.path.join(image_directory, f"{user.username}.jpg")
            cv2.imwrite(image_path, img)

            # Use the face_detector function with the correct argument
            face_locations = face_detector(img, number_of_times_to_upsample)

            if len(face_locations) > 0:
                face_images.append((face_locations[0], user.username))

    return face_images


def check_person_exists_in_database():
    load_faces_in_db()
    cap = cv2.VideoCapture(0)
    images_folder = "images/"

    print("Start")

    knownFace_Images = []

    # Load all the images from the images folder
    for filename in os.listdir(images_folder):
        if filename.endswith(".jpg"):
            knownFace_Image = face_recognition.load_image_file(os.path.join(images_folder, filename))
            knownFace_Encoding = face_recognition.face_encodings(knownFace_Image)[0]
            knownFace_Images.append((knownFace_Encoding, filename))

    x = 0
    detected_person_name = None

    while True:
        try:
            _, frame = cap.read()
            cv2.imwrite("image.jpg", frame)
            unknownFace_Image = face_recognition.load_image_file("abc.jpg")
            unknownFace = face_recognition.face_encodings(unknownFace_Image)[0]

            for knownFace, filename in knownFace_Images:
                try:
                    answer = face_recognition.compare_faces([knownFace], unknownFace)
                except TypeError:
                    continue
                x += 1
                if answer[0]:
                    detected_person_name = os.path.splitext(filename)[0]
                    print(detected_person_name)
                    return detected_person_name

            if detected_person_name is not None:
                break
            elif x < 5:
                return False
        except:
            pass

    return detected_person_name is not None



def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5)  # Set the timeout to 5 seconds

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query

    except sr.UnknownValueError:
        print("Unable to recognize your voice.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return "None"