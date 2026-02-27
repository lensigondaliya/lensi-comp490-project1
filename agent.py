import os
from typing import Any, Dict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent  # updated import

from src.stt import record_microphone_to_wav, convert_wav_to_text
from skills import current_datetime, get_my_bookings, login_access_token

load_dotenv()


def tool_current_time() -> Dict[str, Any]:
    """
    Return the current local date and time information.

    Returns:
        Dictionary containing ISO timestamp, weekday, date, and time.
    """
    return current_datetime()


def tool_my_bookings() -> str:
    """"
    Retrieve and format the authenticated user's meeting reservations.

    Returns:
    A formatted string listing up to 5 upcoming bookings.
    """

    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    if not email or not password:
        return "Missing EMAIL or PASSWORD in .env"

    token = login_access_token(email, password)
    data = get_my_bookings(token)

    if not data:
        return "No bookings found."

    # Format bookings 
    lines = ["Here are your bookings:"]
    for i, b in enumerate(data[:5], start=1):
        room = (
            b.get("meeting_room", {}).get("room_name")
            or "Unknown room"
)
        start = b.get("start_time", "Unknown start")
        end = b.get("end_time", "Unknown end")
        lines.append(f"{i}. {room}: {start} → {end}")

    return "\n".join(lines)

def main():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    tools = [tool_my_bookings, tool_current_time]

    agent = create_agent(llm, tools)

    print("Type your question, or type 'voice' to record, or 'quit' to exit:")

    while True:
        q = input("> ").strip()

        if q.lower() == "quit":
            break

        # VOICE MODE
        if q.lower() == "voice":
            wav_path = "data/mic.wav"
            
            record_microphone_to_wav(wav_path, duration=5, sample_rate=16000)

            q = convert_wav_to_text(wav_path).strip()
            print("\nTRANSCRIPTION:\n", q, "\n")

            if not q:
                print("No speech detected. Try again.\n")
                continue

        result = agent.invoke({"messages": [("user", q)]})
        text = result["messages"][-1].content

        print("\nANSWER:\n", text, "\n")


if __name__ == "__main__":
    main()