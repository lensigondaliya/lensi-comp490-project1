import os
import requests
from typing import Any, Dict, List, Optional, Union


# Expect: export SERVER_URL="http://198.74.62.248:4567"
BASE_URL = (os.getenv("SERVER_URL") or "").rstrip("/")


def _require_base_url() -> None:
    if not BASE_URL:
        raise ValueError("SERVER_URL is not set. In terminal: export SERVER_URL='http://IP:PORT'")


def _auth_headers(token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _short(text: str, n: int = 300) -> str:
    if text is None:
        return ""
    text = str(text)
    return text[:n] + ("..." if len(text) > n else "")


def _extract_access_token(login_json: Any) -> str:
    """
    Be flexible: API responses sometimes look like:
      {"access": "..."} OR {"token": {"access": "..."}} OR {"tokens": {"access": "..."}}
    """
    if isinstance(login_json, dict):
        if isinstance(login_json.get("access"), str):
            return login_json["access"]

        for k in ("token", "tokens", "data"):
            val = login_json.get(k)
            if isinstance(val, dict) and isinstance(val.get("access"), str):
                return val["access"]

    raise ValueError(f"No access token found in login response: {login_json}")


# 1) LOGIN
def login(email: str, password: str) -> Dict[str, Any]:
    _require_base_url()
    url = f"{BASE_URL}/api/v1/member/login/"
    payload = {"email": email, "password": password}

    resp = requests.post(url, json=payload, timeout=20)
    print("LOGIN STATUS:", resp.status_code)
    if not resp.ok:
        print("LOGIN ERROR:", _short(resp.text))

    resp.raise_for_status()
    data = resp.json()
    return data


# 2) LIST ALL ROOMS (handy, and counts as an endpoint)
def list_rooms(token: str) -> List[Dict[str, Any]]:
    _require_base_url()
    url = f"{BASE_URL}/api/v1/meeting-rooms/"
    headers = _auth_headers(token)

    resp = requests.get(url, headers=headers, timeout=20)
    print("LIST ROOMS STATUS:", resp.status_code)
    if not resp.ok:
        print("LIST ROOMS ERROR:", _short(resp.text))

    resp.raise_for_status()
    data = resp.json()
    # Usually list, but some APIs wrap it
    if isinstance(data, dict) and "results" in data and isinstance(data["results"], list):
        return data["results"]
    if isinstance(data, list):
        return data
    return [data]


# 3) GET AVAILABLE ROOMS

def get_available_rooms(token: str, start_time: Optional[str] = None, end_time: Optional[str] = None) -> List[Any]:
    _require_base_url()
    url = f"{BASE_URL}/api/v1/meeting-rooms/available/"
    headers = _auth_headers(token)

    payload: Dict[str, str] = {}
    if start_time:
        payload["start_time"] = start_time
    if end_time:
        payload["end_time"] = end_time

    # 1) Try GET with JSON body (matches “sent in json”)
    resp = requests.get(url, headers=headers, json=payload if payload else None, timeout=20)
    print("AVAILABLE ROOMS STATUS:", resp.status_code)
    if not resp.ok:
        print("AVAILABLE ROOMS ERROR:", _short(resp.text))
    resp.raise_for_status()

    data = resp.json()

    # Normalize output to a list
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "results" in data and isinstance(data["results"], list):
        return data["results"]

    # Some APIs return {"rooms":[...]}
    if isinstance(data, dict) and "rooms" in data and isinstance(data["rooms"], list):
        return data["rooms"]

    return []



# 4) BOOK ROOM
def book_room(
    token: str,
    room_id: int,
    start_time: str,
    end_time: str,
    no_of_persons: int = 1,
) -> Dict[str, Any]:
    """
    IMPORTANT: start_time/end_time must be like: "2026-02-20 10:00 AM"
    Returns:
      On success -> {"ok": True, "status": 200/201, "data": <json>}
      On failure -> {"ok": False, "status": 400/403/404, "error_text": "..."}
    """
    _require_base_url()
    url = f"{BASE_URL}/api/v1/meeting-rooms/{room_id}/book/"
    headers = _auth_headers(token)
    payload = {"start_time": start_time, "end_time": end_time, "no_of_persons": no_of_persons}

    resp = requests.post(url, headers=headers, json=payload, timeout=20)
    print("BOOK STATUS:", resp.status_code)
    if not resp.ok:
        print("BOOK ERROR:", _short(resp.text))
        return {"ok": False, "status": resp.status_code, "error_text": resp.text}

    # success
    try:
        return {"ok": True, "status": resp.status_code, "data": resp.json()}
    except Exception:
        return {"ok": True, "status": resp.status_code, "data": resp.text}


# 5) LIST MY BOOKINGS  (THIS IS THE ENDPOINT YOU HAD WRONG BEFORE)
def get_my_bookings(token: str) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    _require_base_url()
    url = f"{BASE_URL}/api/v1/meeting-rooms/my-bookings/"
    headers = _auth_headers(token)

    resp = requests.get(url, headers=headers, timeout=20)
    print("MY BOOKINGS STATUS:", resp.status_code)
    if not resp.ok:
        print("MY BOOKINGS ERROR:", _short(resp.text))

    resp.raise_for_status()
    return resp.json()


# 6) CANCEL BOOKING
def cancel_booking(token: str, booking_id: int) -> Dict[str, Any]:
    _require_base_url()
    url = f"{BASE_URL}/api/v1/meeting-rooms/{booking_id}/cancel-booking/"
    headers = _auth_headers(token)

    resp = requests.delete(url, headers=headers, timeout=20)
    print("CANCEL STATUS:", resp.status_code)
    if not resp.ok:
        print("CANCEL ERROR:", _short(resp.text))
        return {"ok": False, "status": resp.status_code, "error_text": resp.text}

    try:
        return {"ok": True, "status": resp.status_code, "data": resp.json()}
    except Exception:
        return {"ok": True, "status": resp.status_code, "data": resp.text}


# Helper: do login + return access token as a string
def login_access_token(email: str, password: str) -> str:
    data = login(email, password)
    return _extract_access_token(data)
