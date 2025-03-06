import noisereduce as nr
import librosa
import soundfile as sf
import numpy as np

# Load audio file
file_path = "meeting1.mp3"
y, sr = librosa.load(file_path, sr=None)

# Process audio in chunks (e.g., 1-second windows)
chunk_size = sr  # 1 second
denoised_audio = np.array([])

for i in range(0, len(y), chunk_size):
    chunk = y[i : i + chunk_size]
    reduced_chunk = nr.reduce_noise(y=chunk, sr=sr, prop_decrease=0.8)
    denoised_audio = np.concatenate((denoised_audio, reduced_chunk))

# Save the denoised file
sf.write("denoised_audio.wav", denoised_audio, sr)
print("Denoised audio saved successfully!")
