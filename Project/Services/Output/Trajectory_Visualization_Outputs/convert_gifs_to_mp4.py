import os
from moviepy import VideoFileClip

if __name__ == '__main__':
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for file in files:
        if file.endswith(".gif"):
            clip = VideoFileClip(file)
            clip.write_videofile(file.replace('.gif', '.mp4'))
