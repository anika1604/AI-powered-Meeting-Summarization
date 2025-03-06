import whisper  

# Load the model with FP32 precision
model = whisper.load_model("base", device="cpu")  # Ensure it runs on CPU

# Transcribe the audio file
result = model.transcribe("amplified_audio.wav")

# Print the transcribed text
print(result["text"])
