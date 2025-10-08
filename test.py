import speech_recognition as sr

import hardware_routes

recognizer = sr.Recognizer()


with sr.Microphone() as source:
    print("Listening...")
    audio = recognizer.listen(source)

try:
    command = recognizer.recognize_google(audio)
    print("Command:", command)

    # Process the command and trigger the appropriate function
    if "turn on light" in command:
        print(11)
        hardware_routes.turn_on_light()
    elif "open door" in command:
        print()
    else:
        print(1)
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("Error: {0}".format(e))
