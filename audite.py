import random
from datetime import datetime

import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone, currentDateTime):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    flacName = "microphone-results-"
    flacName += currentDateTime
    flacName += ".flac"
    #Save the results as a FLAC file.
    with open(flacName, "wb") as f:
        f.write(audio.get_flac_data())
        f.close()

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    for i in range(5):
        while(1):
            now = datetime.now()
            currentDateTime = now.strftime("%m-%d-%Y-%H:%M:%S")
            print("Please say something!")
            spoken = recognize_speech_from_mic(recognizer, microphone, currentDateTime)
            if spoken["transcription"]:
                break
            if not guess["success"]:
                print("I didn't catch that. What did you say?\n")
                break
            if guess["error"]:
                print("ERROR: {}".format(guess["error"]))
                break
        print("You said: {}".format(spoken["transcription"]))
        toWrite = "["
        toWrite += currentDateTime
        toWrite += "] : "
        toWrite += spoken["transcription"]
        toWrite += "\n"
        with open("spoken log.txt", "a") as myfile:
            myfile.write(toWrite)
            myfile.close()
