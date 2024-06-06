import speech_recognition as sr
import pyttsx3
import time
from groq import Groq

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def SpeakText(text):
    # Convert text to speech
    engine.say(text)
    # Play the speech
    engine.runAndWait()

def record_text(language='en-US'):  # Default language set to English (United States)
    # Loop in case of error
    while True:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                # Listens for the user's input
                audio2 = r.listen(source2)
                # Using Google to recognize audio with specified language
                MyText = r.recognize_google(audio2, language=language)
                MyText = MyText.lower()
                print("USER:\t", MyText)
                return MyText
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Please repeat your question.")
            return None

# Function to output text
def output_text(text):
    with open("output.txt", "a") as f:
        f.write(text + "\n")

# Access our Groq account
client = Groq(api_key="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")

# Conversation history
mssgs = [
    {"role": "system", "content": "your name is oris"},
    {"role": "system", "content": "your answer is too long, give me a short answer"},
    {"role": "system", "content": "only answer the thing that is being asked, not more, not less, with a total of 15 words for the explanation"},
]

# Function to reply to user question
def groqReply(question):
    mssgs.append({"role": "user", "content": question})
    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=mssgs,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    respon = completion.choices[0].message.content
    mssgs.append({"role": "assistant", "content": respon})
    return respon

while True:
    text = record_text(language='en-US')  # You can specify the language here
    if text:
        output_text(text)
        gAnswer = groqReply(text)
        print("AI:\t", gAnswer)
        SpeakText(gAnswer)
    # Introduce a 1-second delay before listening for input again
    time.sleep(1)
