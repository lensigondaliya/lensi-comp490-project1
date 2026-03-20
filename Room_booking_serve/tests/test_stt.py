import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from stt import convert_wav_to_text


def test_speech_to_text_returns_string():
    audio_file = Path(__file__).resolve().parents[1] / "data" / "voice4.wav"
    result_text = convert_wav_to_text(str(audio_file))

    assert isinstance(result_text, str)
    assert len(result_text) > 0