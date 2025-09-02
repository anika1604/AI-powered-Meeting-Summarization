from moviepy.editor import *

# Load the mp4 file
video = VideoFileClip("example.mp4")

# Extract audio from video
video.audio.write_audiofile("example.mp3")