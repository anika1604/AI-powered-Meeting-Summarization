import librosa
import soundfile as sf
import numpy as np

# Load the audio file
audio_file = "denoised_audio.wav"
y, sr = librosa.load(audio_file, sr=16000)  # Load with a fixed sample rate

# Increase volume (amplify by a factor)
amplification_factor = 5.0  # Increase as needed
y_amplified = np.clip(y * amplification_factor, -1.0, 1.0)  # Prevent distortion

# Save the amplified audio
amplified_file = "amplified_audio.wav"
sf.write(amplified_file, y_amplified, sr)

print(f"Saved amplified file as {amplified_file}")
