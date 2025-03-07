from flask import Flask, render_template, request, jsonify
import os
import json
from dotenv import load_dotenv
from groq import Groq

app = Flask(__name__)

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

    # Initialize the Groq client
client = Groq(
    api_key=my_api_key,
)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




def read_json_file():
    # Path to the primary and default JSON files
    primary_file_path = "json_responses/meeting_summary.json"
    default_file_path = "json_responses/default_json.json"
    
    # Check if the primary file exists
    if os.path.exists(primary_file_path):
        file_path = primary_file_path
    else:
        # If the primary file doesn't exist, use the default file
        file_path = default_file_path
    
    # Read and return the JSON data from the selected file
    with open(file_path, "r") as file:
        data = json.load(file)
    
    return data

def read_transcripts():
    primary_path = "transcription/transcription_output.txt"
    secondary_path = "transcription/default.txt"

    if os.path.exists(primary_path):
        file_path = primary_path
    else:
        file_path = secondary_path

    with open(file_path, 'r') as file:
        data = file.read()

    return data

def create_transcripts():

    # Specify the path to the audio file
    filename_audio = os.path.dirname(__file__) + "/uploads/recorded_meeting.mp3"

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
                    "content": '''You are a meeting summariser  API capable generating summary of meetings that responds in JSON.Scritly follow the json format.Do not include any excess keys.  The JSON schema should include {"summary": {""},"todo_work": [{"assignee":{},"work":{[""]}]},}'''
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


   
def export_response_as_json(responses_output = "responses_output.txt"):
    filename_response = os.path.dirname(__file__) + f"/responses/{responses_output}"
    cleaned_text = ""
    with open(filename_response, "rb") as file:
        contents = file.read()
        contents_decoded = contents.decode('utf-8')
        start = contents_decoded.find('<think>') 
        end = contents_decoded.find('</think>', start)

        if start != -1 and end != -1: 
            cleaned_text = contents_decoded[:start] + contents_decoded[end + len('</think>'):] 
        else: 
            cleaned_text = contents_decoded
        cleaned_text = cleaned_text.replace("json", "")
        cleaned_text = cleaned_text.replace("```", "")
        cleaned_text = cleaned_text.strip()
        # print(f"{cleaned_text}")
    # Folder path
    folder_path = 'json_responses'

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Full file path including the folder and filename
    filename = os.path.join(folder_path, 'meeting_summary.json')

    # Writing the data to a JSON file

    with open(filename, "w") as output_file:
        output_file.write(cleaned_text)


@app.route('/index')
def index():
    json_data = read_json_file()
    with open('transcription/transcription_output.txt', 'r') as file:
        file_contents = file.read()
        return render_template("index.html", data=file_contents)

@app.route('/')
def home():
    json_data = read_json_file()
    file_contents = read_transcripts()
    return render_template('home.html', data=json_data, file_contents=file_contents)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the request contains the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # If the user does not select a file or the file is empty
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Check if the file is allowed
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], f"recorded_meeting.{file.filename.rsplit('.', 1)[1].lower()}")
        file.save(filename)
        create_transcripts()
        get_response()
        export_response_as_json()

        # json_data = read_json_file()
        # return render_template('index.html', data=json_data)
        # Call your function to process the uploaded file here
        return jsonify({"message": "File successfully uploaded", "filename": file.filename}), 200
    else:
        return jsonify({"error": "Invalid file format"}), 400


if __name__ == '__main__':
    app.run(debug=True)