import os
import streamlit as st
import subprocess

# Function to download videos from YouTube
def download_videos(artist_name, num_videos):
    command = f"youtube-dl --extract-audio --audio-format mp3 --output 'videos/%(title)s.%(ext)s' --max-downloads {num_videos} 'ytsearch20:{artist_name}'"
    subprocess.run(command, shell=True)

# Function to trim audio files
def trim_audios():
    os.makedirs("audios", exist_ok=True)
    for video_file in os.listdir("videos"):
        audio_file = os.path.splitext(video_file)[0] + ".mp3"
        input_path = os.path.join("videos", audio_file)
        output_path = os.path.join("audios", audio_file)
        subprocess.run(f"ffmpeg -y -i {input_path} -ss 0 -t 30 {output_path}", shell=True)

# Function to merge audio files
def merge_audios():
    audio_files = " ".join([os.path.join("audios", file) for file in os.listdir("audios")])
    subprocess.run(f"ffmpeg -y -i 'concat:{audio_files}' -c copy merged_audio.mp3", shell=True)

# Function to send email
def send_email(receiver_email):
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"
    
    command = f"echo 'Please find the attached merged audio file.' | mail -s 'Merged Audio File' -A 'merged_audio.mp3' -r {sender_email} {receiver_email}"
    subprocess.run(command, shell=True)

# Streamlit web app
def main():
    st.title("YouTube Video Downloader and Audio Merger")

    artist_name = st.text_input("Enter artist name:", "sharry maan")
    num_videos = st.slider("Number of videos to download:", 1, 20, 5)
    receiver_email = st.text_input("Enter receiver email address:")

    if st.button("Download and Merge"):
        # Step 1: Download videos
        st.write("Downloading videos...")
        download_videos(artist_name, num_videos)

        # Step 2: Convert videos to audio and extract first 30 seconds
        st.write("Trimming audios...")
        trim_audios()

        # Step 3: Merge audio files into a single file
        st.write("Merging audios...")
        merge_audios()

        # Step 4: Send email with the merged audio file attached
        st.write("Sending email...")
        send_email(receiver_email)

        st.success("Process completed successfully!")

        # Clean up temporary folders
        shutil.rmtree("videos")
        shutil.rmtree("audios")
        os.remove("merged_audio.mp3")

if __name__ == "__main__":
    main()
