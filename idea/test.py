import os
import speech_recognition as sr
from pydub import AudioSegment

def convert_m4a_to_wav(m4a_file, wav_file):
    audio = AudioSegment.from_file(m4a_file, format="m4a") #m4a mp3 here
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    audio.export(wav_file, format="wav")

def transcribe_audio(wav_file, chunk_length_ms=60000): #ms60000is 60s
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_wav(wav_file)
    total_length_ms = len(audio)
    print(f"Total audio length: {total_length_ms // 1000} seconds")

    for start in range(0, total_length_ms, chunk_length_ms):
        end = min(start + chunk_length_ms, total_length_ms)
        chunk = audio[start:end]
        chunk.export("temp_chunk.wav", format="wav")
        print(f"transcribing chunk from {start // 1000} to {end // 1000} seconds")
        with sr.AudioFile("temp_chunk.wav") as source:
            audio_data = recognizer.record(source)
            try:
                korean_text = recognizer.recognize_google(audio_data, language='ko-KR')
                print("kr:")
                print(korean_text)
            except sr.UnknownValueError:
                print("cant scan kr.")
            except sr.RequestError as e:
                print(f"error with google: {e}") #china -> use proxy

if __name__ == "__main__":
    m4a_file = "mp3.m4a"
    wav_file = "converted_audio.wav"

    convert_m4a_to_wav(m4a_file, wav_file)
    if os.path.exists(wav_file):
        print(f"WAV file created: {wav_file}")
        # Transcribe the audio in chunks
        transcribe_audio(wav_file)
    else:
        print("WAV file didnt create error.") #file permisson or dependencyt
