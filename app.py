import os
from dotenv import load_dotenv
from flask import Flask
from groq import Groq


load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")


# Initialize the Groq client
client = Groq(
    api_key=my_api_key,
)



# Specify the path to the audio file
filename = os.path.dirname(__file__) + "/audio_samples/sample-0.mp3" # Replace with your audio file!


folder_path = "transcription"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

with open(filename, "rb") as file:
    transcription = client.audio.transcriptions.create(
        file=(filename, file.read()),
        model="distil-whisper-large-v3-en",
    #   prompt="Specify context or spelling",
        response_format="verbose_json",
    )
    
    transcript_text = transcription.text
    
    output_path = os.path.join(folder_path, "transcription_output.txt")
    with open(output_path, "w") as output_file:
        output_file.write(transcript_text)
    
    print(f"Transcription saved to '{output_path}'.")
