import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

    # Initialize the Groq client
client = Groq(
    api_key=my_api_key,
)

def create_transcripts():


    # Specify the path to the audio file
    filename_audio = os.path.dirname(__file__) + "/AUD_Samples/John_Rachel.mp3"


    folder_path = "transcription"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(filename_audio, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(filename_audio, file.read()),
            model="distil-whisper-large-v3-en",
            prompt="you are an api that can generate transcripts of meetings. Please generate transcript in dialogue form",
            response_format="verbose_json",
        )
        
        transcript_text = transcription.text
        
        output_path = os.path.join(folder_path, "transcription_output.txt")
        with open(output_path, "w") as output_file:
            output_file.write(transcript_text)
        
        print(f"Transcription saved to '{output_path}'.")
    

def get_response():
    filename_transcript = os.path.dirname(__file__) + "/transcription/transcription_output.txt"
    folder_path_responses = "responses"
    if not os.path.exists(folder_path_responses):
        os.makedirs(folder_path_responses)

    with open(filename_transcript, "rb") as file:
        contents = file.read()
        completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a meeting summariser  API capable generating summary of meetings that responds in JSON.  The JSON schema should include\n{\n\"summary\":{\n}\n\"todo_work\":{\n}\n}\n"
                },
                {
                    "role": "assistant",
                    "content": ""
                },
                {
                    "role": "user",
                    "content": f"generate a summary of this meeting don't include any excess keys in the json other than what is specified:\n\n {contents}"
                }
            ],
            temperature=0.6,
            max_completion_tokens=4096,
            top_p=0.95,
            stream=True,
            stop=None,
        )

        response = ""
        # print(response)

        for chunk in completion:
            partial_response = (chunk.choices[0].delta.content or "")
            response += partial_response

        output_path = os.path.join(folder_path_responses, "responses_output.txt")
        with open(output_path, "w") as output_file:
            output_file.write(response)
    



