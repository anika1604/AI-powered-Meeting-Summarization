import os

def export_response_as_json(responses_output):
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


    # print(f"JSON data has been saved to {filename}")

if __name__ == "__main__":
    export_response_as_json("responses_output.txt")


