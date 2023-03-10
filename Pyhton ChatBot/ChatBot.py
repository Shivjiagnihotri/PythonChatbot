import openai
import speech_recognition as sr
import pyttsx3

# Set up the OpenAI API client with your API key
openai.api_key = "YOUR_API_KEY_HERE"

# Set up the speech recognition engine
r = sr.Recognizer()

# Set up the text-to-speech engine
engine = pyttsx3.init()
counter = 1
# Define a function to take speech input and generate a spoken response
def talk(counter):
    # Output the greeting message as spoken text
    if counter == 1:
        greeting = "Hello, how can I assist you?"
    if counter == 2:
        greeting = "Good to see you again! How can I assist you?"
    else:
        greeting = "Can you please repeat your question?"
    print(greeting)
    engine.say(greeting)
    engine.runAndWait()

    # Listen for speech input from the user
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        # Use the OpenAI API to generate a response to the user's input
        prompt = r.recognize_google(audio)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            temperature=0.5,
        )
        answer = response.choices[0].text.strip()

        # Output the response as spoken text
        print("You said:", prompt)
        print("AI says:", answer)
        engine.say(answer)
        engine.runAndWait()

    except sr.UnknownValueError:
        # Handle speech recognition errors
        print("Sorry, I didn't understand that.")
        engine.say("Sorry, I didn't understand that.")
        engine.runAndWait()
        talk(3) #Call the function recursively to get the repeated question
    except sr.RequestError as e:
        print("Could not request results from speech recognition service; {0}".format(e))
        engine.say("Sorry, I'm having trouble connecting to the speech recognition service. Please try again later.")
        engine.runAndWait()

# Continuously prompt the user for input until they say "stop"
while True:
    talk(2)
    with sr.Microphone() as source:
        audio = r.listen(source)
        prompt = r.recognize_google(audio)
        if prompt.lower() == "stop":
            break
