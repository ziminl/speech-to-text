import os
import speech_recognition as sr
from pydub import AudioSegment

def convert_m4a_to_wav(m4a_file, wav_file):
    audio = AudioSegment.from_file(m4a_file, format="m4a")
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    audio.export(wav_file, format="wav")

def combine_strings(str1, str2):
    prefix = str2[:6]
    index = str1.find(prefix)
    if index != -1:
        modified_str1 = str1[:index]
        combined = modified_str1 + str2
        return combined
    else:
        return str1 + " " + str2

def transcribe_audio(wav_file, chunk_length_ms=60000, overlap_ms=30000):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_wav(wav_file)
    total_length_ms = len(audio)
    print(f"Total audio length: {total_length_ms // 1000} seconds")

    recognized_texts = []
    
    for start in range(0, total_length_ms - chunk_length_ms + 1, chunk_length_ms - overlap_ms):
        end = start + chunk_length_ms
        chunk = audio[start:end]
        chunk.export("temp_chunk.wav", format="wav")
        
        print(f"Transcribing chunk from {start // 1000} to {end // 1000} seconds...")
        
        with sr.AudioFile("temp_chunk.wav") as source:
            audio_data = recognizer.record(source)
            try:
                korean_text = recognizer.recognize_google(audio_data, language='ko-KR')
                print(korean_text)
                recognized_texts.append(korean_text)
            except sr.UnknownValueError:
                print("cant scan kr.")
            except sr.RequestError as e:
                print(f"error with google: {e}") #china -> use proxy

    merged_text = merge_transcripts(recognized_texts)

    with open("1.txt", "w", encoding="utf-8") as f:
        f.write(merged_text)

    print("Transcription saved to 1.txt")

def merge_transcripts(texts):
    if not texts:
        return ""
    combined = texts[0]
    for current_text in texts[1:]:
        combined = combine_strings(combined, current_text)
    return combined

if __name__ == "__main__":
    m4a_file = "mp3.m4a"
    wav_file = "converted_audio.wav"

    convert_m4a_to_wav(m4a_file, wav_file)

    if os.path.exists(wav_file):
        print(f"WAV file created: {wav_file}")
        transcribe_audio(wav_file)
    else:
        print("WAV file didnt create error.") #file permisson or dependencyt
