import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


import requests


# def _require_base_url() -> str:
#     """
#     Construct authorization headers for authenticated API requests.

#     Args:
#         token: JWT access token.

#     Returns:
#         Dictionary containing Authorization header.
#     """
#     base = os.getenv("SERVER_URL") or os.getenv("BASE_URL") or os.getenv("SERVER")
#     if not base:
#         raise RuntimeError("Missing SERVER_URL in environment (.env).")
#     return base.rstrip("/")

def _require_base_url() -> str:
    return "http://127.0.0.1:8000"

def _short(text: str, limit: int = 400) -> str:
    text = text or ""
    return text if len(text) <= limit else text[:limit] + "..."


def _auth_headers(token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _extract_access_token(login_json: Any) -> str:
    """
    Extract the access token from the login response.
    Supports different possible response formats returned by the API.
    """
    if isinstance(login_json, dict):
        if isinstance(login_json.get("access"), str):
            return login_json["access"]

        tok = login_json.get("token")
        if isinstance(tok, str):
            return tok
        if isinstance(tok, dict) and isinstance(tok.get("access"), str):
            return tok["access"]

     
        if isinstance(tok, dict) and isinstance(tok.get("token"), dict):
            inner = tok.get("token")
            if isinstance(inner.get("access"), str):
                return inner["access"]

        data = login_json.get("data")
        if isinstance(data, dict) and isinstance(data.get("access"), str):
            return data["access"]

    raise ValueError(f"No access token found in login response: {login_json}")


def current_datetime() -> Dict[str, Any]:
    """
    Return current local date/time info (useful for interpreting 'today', 'tomorrow', etc.)
    """
    now = datetime.now()
    return {
        "iso": now.isoformat(timespec="seconds"),
        "weekday": now.strftime("%A"),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
    }


def login(email: str, password: str) -> Dict[str, Any]:
    """Authenticate the user and return the login response JSON."""
    base = _require_base_url()
    url = f"{base}/api/v1/member/login/"
    payload = {"email": email, "password": password}

    resp = requests.post(url, json=payload, timeout=20)
    resp.raise_for_status()
    return resp.json()


def login_access_token(email: str, password: str) -> str:
    """Log in and return JWT access token."""
    data = login(email, password)
    return _extract_access_token(data)


def list_rooms(token: str) -> List[Dict[str, Any]]:
    """
    Retrieve a list of all meeting rooms available on the server.

    Args:
        token: JWT access token for authentication.

    Returns:
        A list of room dictionaries as returned by the API.
    """
    base = _require_base_url()
    url = f"{base}/api/v1/meeting-rooms/"
    resp = requests.get(url, headers=_auth_headers(token), timeout=20)
    print("LIST ROOMS STATUS:", resp.status_code)
    if not resp.ok:
        print("LIST ROOMS ERROR:", _short(resp.text))
    resp.raise_for_status()
    data = resp.json()

    
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("results"), list):
        return data["results"]
    return [data]


def get_available_rooms(
    token: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Get available rooms for a time window.
    """
    base = _require_base_url()
    url = f"{base}/api/v1/meeting-rooms/available/"
    headers = _auth_headers(token)

    payload: Dict[str, str] = {}
    if start_time:
        payload["start_time"] = start_time
    if end_time:
        payload["end_time"] = end_time

    resp = requests.get(url, headers=headers, json=payload if payload else None, timeout=20)
    print("AVAILABLE ROOMS STATUS:", resp.status_code)
    if not resp.ok:
        print("AVAILABLE ROOMS ERROR:", _short(resp.text))
    resp.raise_for_status()
    data = resp.json()

    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("results"), list):
        return data["results"]
    return [data]


def get_my_bookings(token: str) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """Fetch all bookings for the authenticated user."""
    base = _require_base_url()
    url = f"{base}/api/v1/meeting-rooms/my-bookings/"
    resp = requests.get(url, headers=_auth_headers(token), timeout=20)
    print("MY BOOKINGS STATUS:", resp.status_code)
    if not resp.ok:
        print("MY BOOKINGS ERROR:", _short(resp.text))
    resp.raise_for_status()
    return resp.json()


def book_room(
    token: str,
    room_id: int,
    start_time: str,
    end_time: str,
    no_of_persons: int = 1,
) -> Dict[str, Any]:
    """
    Book a meeting room for a specified time range.
    """
    base = _require_base_url()
    url = f"{base}/api/v1/meeting-rooms/{room_id}/book/"

    payload = {
        "start_time": start_time,
        "end_time": end_time,
        "no_of_persons": no_of_persons,
    }

    resp = requests.post(url, headers=_auth_headers(token), json=payload, timeout=20)

    if not resp.ok:
        return {"ok": False, "status": resp.status_code, "error_text": resp.text}

    try:
        return {"ok": True, "status": resp.status_code, "data": resp.json()}
    except Exception:
        return {"ok": True, "status": resp.status_code, "data": resp.text}


def cancel_booking(token: str, booking_id: int) -> Dict[str, Any]:
    """Cancel a booking by ID."""
    base = _require_base_url()
    url = f"{base}/api/v1/meeting-rooms/{booking_id}/cancel-booking/"
    resp = requests.delete(url, headers=_auth_headers(token), timeout=20)
    print("CANCEL STATUS:", resp.status_code)
    if not resp.ok:
        print("CANCEL ERROR:", _short(resp.text))
        return {"ok": False, "status": resp.status_code, "error_text": resp.text}

    try:
        return {"ok": True, "status": resp.status_code, "data": resp.json()}
    except Exception:
        return {"ok": True, "status": resp.status_code, "data": resp.text}