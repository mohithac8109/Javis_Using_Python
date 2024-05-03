import speech_recognition as sr
import pyttsx3
import datetime
import requests
import webbrowser

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)
            return command
        except sr.UnknownValueError:
            print("Sorry, I didn't understand. Please try again.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

def get_current_time():
    current_time = datetime.datetime.now().strftime("%H:%M %p")
    return f"The current time is {current_time}."

def get_weather():
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    city = "YOUR_CITY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    try:
        response = requests.get(url)
        data = response.json()
        weather_description = data["weather"][0]["description"]
        temperature = round(data["main"]["temp"] - 273.15, 2)  # Convert Kelvin to Celsius
        return f"The weather is {weather_description} and the temperature is {temperature} degrees Celsius."
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return "Sorry, I couldn't fetch the weather information."

def open_webpage(url):
    webbrowser.open(url)
    return f"Opening {url}."

def open_app(app_name):
    return f"Opening {app_name}."

def process_command(command):
    if "hello" in command:
        return "Hello! How can I assist you today?"
    elif "time" in command:
        return get_current_time()
    elif "weather" in command:
        return get_weather()
    elif "open web page" in command:
        speak("Sure, which webpage would you like to open?")
        webpage_url = listen()
        return open_webpage(webpage_url)
    elif "open app" in command:
        speak("Sure, which app would you like to open?")
        app_name = listen()
        return open_app(app_name)
    elif "goodbye" in command or "bye" in command:
        return "Goodbye! Have a great day."
    else:
        return "I'm not sure how to respond to that command."

if __name__ == "__main__":
    speak("Hello! How can I assist you today?")

    while True:
        command = listen()
        if command:
            if "goodbye" in command or "bye" in command:
                speak("Goodbye! Have a great day.")
                break
            else:
                response = process_command(command)
                speak(response)
