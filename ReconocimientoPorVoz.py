import openai
import speech_recognition as sr
import pyttsx3
import time 

# Inicializa la API de OpenAI
openai.api_key = "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"

# Inicializa el motor de texto a voz
engine = pyttsx3.init()

# Configura la voz en español para el motor de texto a voz
voices = engine.getProperty('voices')
spanish_voice = next((voice.id for voice in voices if "spanish" in voice.languages), None)
if spanish_voice is not None:
    engine.setProperty('voice', spanish_voice)

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source) 
    try:
        return recognizer.recognize_google(audio, language="es")
    except sr.UnknownValueError:
        print("No se ha podido reconocer el audio")
    except sr.RequestError as e:
        print(f"No se ha podido conectar con el servidor de Google: {e}")

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    salir = False
    while not salir:
        # Espera a que el usuario diga "Hola"
        print("Di 'Hola' para empezar a grabar o 'Adiós' para salir")
        speak_text("Di 'Hola' para empezar a grabar o 'Adiós' para salir")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio, language="es")
                if transcription.lower() == "hola":
                    # Graba el audio
                    filename = "input.wav"
                    print("Dime que quieres mozo")
                    speak_text("En que puedo ayudarte?")
                    
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                    # Transcribe el audio a texto 
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"Yo: {text}")
                        
                        # Genera la respuesta
                        response = generate_response(text)
                        print(f"El bot dice: {response}")
                            
                        # Lee la respuesta utilizando el motor de texto a voz
                        speak_text(response)
                elif transcription.lower() == "adiós" or transcription.lower() == "salir":
                    print("Adiós!")
                    speak_text("Adiós!")
                    salir = True
            except sr.UnknownValueError:
                print("No se ha podido reconocer el audio")
            except sr.RequestError as e:
                print(f"No se ha podido conectar con el servidor de Google: {e}")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
