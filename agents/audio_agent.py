import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def transcribe_audio(audio_file) -> str:
    """
    Takes an audio file from Streamlit's file uploader,
    sends it to Groq's Whisper endpoint, returns the transcript as text.
    Supports mp3, m4a, wav, webm, ogg, flac, mp4 (max 25MB).
    """
    # Use the actual filename so Groq can detect the format from the extension
    filename = getattr(audio_file, "name", "meeting_audio.m4a")

    transcription = client.audio.transcriptions.create(
        file=(filename, audio_file.read()),
        model="whisper-large-v3-turbo",
        response_format="text",
        language="en"
    )
    return transcription