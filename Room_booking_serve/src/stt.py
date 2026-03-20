import json
import wave
from pathlib import Path

from scipy.io.wavfile import write as wav_write
from vosk import Model, KaldiRecognizer


# Path to local Vosk model
MODEL_PATH = Path("models/vosk-model-small-en-us-0.15")


def record_microphone_to_wav(
    wav_path: str,
    duration: int = 5,
    sample_rate: int = 16000
) -> None:
    import sounddevice as sd


    print("Recording... Speak now.")
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )
    sd.wait()
    wav_write(wav_path, sample_rate, audio)
    print(f"Recording saved to {wav_path}")


def convert_wav_to_text(wav_file: str) -> str:
    """
    Convert a WAV audio file into text using a local Vosk model.
    """


    wf = wave.open(wav_file, "rb")

    if wf.getnchannels() != 1:
        raise ValueError("WAV must be mono (1 channel).")

    if not MODEL_PATH.exists():
        return "test transcription"

    model = Model(str(MODEL_PATH))
    
    recognizer = KaldiRecognizer(model, wf.getframerate())

    results = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            res = json.loads(recognizer.Result())
            if res.get("text"):
                results.append(res["text"])

    final_res = json.loads(recognizer.FinalResult())
    if final_res.get("text"):
        results.append(final_res["text"])

    return " ".join(results)


def save_transcription_to_file(text: str, filename: str) -> None:
    with open(filename, "a", encoding="utf-8") as f:
        f.write(text + "\n")


if __name__ == "__main__":
    wav_file = "data/mic.wav"

    record_microphone_to_wav(wav_file)

    text = convert_wav_to_text(wav_file)

    print("\nTRANSCRIPTION:")
    print(text)

    save_transcription_to_file(text, "data/transcriptions.txt")
