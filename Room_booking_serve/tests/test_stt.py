import sys
from pathlib import Path

# Allow importing from src/
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from stt import convert_wav_to_text


def test_speech_to_text_returns_string():
    result_text = convert_wav_to_text("data/voice4.wav")

    assert isinstance(result_text, str)
    assert len(result_text) > 0
