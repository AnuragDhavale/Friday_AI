import speech_recognition as sr
import os
import webbrowser
import openai
import datetime
import pyttsx3

chatStr = ""


# Function to chat using OpenAI
def chat(query):
    global chatStr
    openai.api_key = os.getenv("sk-proj-p1jiRlZV1YSX8YaNE1IWT3BlbkFJspdlnuPeOjuDSbtavo9m")  # Use environment variable for the API key
    chatStr += f"User: {query}\nAssistant: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    response_text = response["choices"][0]["text"].strip()
    say(response_text)
    chatStr += f"{response_text}\n"
    return response_text


# Function to generate AI response
def ai(prompt):
    openai.api_key = os.getenv("sk-proj-p1jiRlZV1YSX8YaNE1IWT3BlbkFJspdlnuPeOjuDSbtavo9m")
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)


# Function to say text using pyttsx3
def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Function to take voice command from user
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            say("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            say("Sorry, my speech service is down.")
            return ""


if __name__ == '__main__':
    print('Welcome to Friday AI')
    say("Welcome to Friday AI")
    while True:
        query = takeCommand()
        if not query:
            continue

        # Commands to open websites
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"]
        ]
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]}...")
                webbrowser.open(site[1])

        # Command to play music
        if "play music" in query.lower():
            musicPath = r"C:\Users\lenov\Downloads\music.mp3"
            if os.path.exists(musicPath):
                os.startfile(musicPath)
            else:
                say("Music file not found.")

        # Command to tell time
        elif "tell time" in query.lower():
            time_now = datetime.datetime.now().strftime("%H:%M")
            say(f"The time is {time_now}")

        # Command to watch movie (assumes path is correct and updated)
        elif "watch movie" in query.lower():
            movie_path = r"E:\Movies and TV Shows\The Batman.mkv"
            if os.path.exists(movie_path):
                os.startfile(movie_path)
            else:
                say("Movie directory not found.")

        # Command to open an application (example given for macOS)
        elif "play game" in query.lower():
            app_path = r"D:\Games\Counter-Strike Condition Zero 1.2 build 2771"
            if os.path.exists(app_path):
                os.startfile(app_path)
            else:
                say("game not found.")

        # Command to interact with AI
        elif "using artificial intelligence" in query.lower():
            ai(prompt=query)

        # Command to quit the program
        elif "friday quit" in query.lower():
            say("Goodbye!")
            break

        # Command to reset chat history
        elif "reset chat" in query.lower():
            chatStr = ""
            say("Chat history reset.")

        # General chat
        else:
            chat(query)
