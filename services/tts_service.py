#!/bin/py
from gtts import gTTS

def create_audio(text, filename):
    try:
        # Create an audio file from the text
        tts = gTTS(text=text, lang='en')
        
        # Save the audio file
        tts.save(filename)
        
        print(f"Audio file created and saved as {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    text = "Hello, welcome to PictoTale."
    create_audio(text, filename='speech.mp3')
