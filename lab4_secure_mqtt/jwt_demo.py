"""
Lab 4 — Part 2 Standalone: JWT Token Generation and Validation
Demonstrates RS256 JWT create → sign → verify WITHOUT any MQTT broker.

Run this first to confirm PyJWT and key files are working correctly.

Prerequisites:
    bash generate_keys.sh      # creates device_private_key.pem + device_public_key.pem
    pip install -r requirements.txt
"""

import datetime
import jwt                         # PyJWT

PRIVATE_KEY_FILE = "device_private_key.pem"
PUBLIC_KEY_FILE  = "device_public_key.pem"
ALGORITHM        = "RS256"
DEVICE_ID        = "esp32-001"


def load_keys():
    with open(PRIVATE_KEY_FILE) as f:
        private = f.read()
    with open(PUBLIC_KEY_FILE) as f:
        public = f.read()
    return private, public


def make_token(private_key: str, data: dict, expires_in_minutes: int = 5) -> str:
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    payload = {
        "device_id": DEVICE_ID,
        "scope":     "telemetry:write",
        "data":      data,
        "iat":       now,
        "exp":       now + datetime.timedelta(minutes=expires_in_minutes),
    }
    return jwt.encode(payload, private_key, algorithm=ALGORITHM)


def verify_token(token: str, public_key: str) -> dict:
    return jwt.decode(token, public_key, algorithms=[ALGORITHM])


def main():
    print("=== Lab 4 — JWT Demo ===\n")

    private_key, public_key = load_keys()
    print(f"Keys loaded from '{PRIVATE_KEY_FILE}' and '{PUBLIC_KEY_FILE}'")

    # ── Create and sign a token ──────────────────────────────────
    sensor_data = {"temp_c": 24.5, "hum_pct": 58.3}
    token = make_token(private_key, sensor_data)
    print(f"\n[1] Token created (RS256, 5-min expiry):")
    print(f"    {token[:60]}...  ({len(token)} chars)")

    # ── Verify valid token ───────────────────────────────────────
    print("\n[2] Verifying valid token...")
    try:
        claims = verify_token(token, public_key)
        print(f"    OK — device_id={claims['device_id']}, data={claims['data']}")
    except jwt.PyJWTError as e:
        print(f"    FAIL: {e}")

    # ── Simulate expired token ────────────────────────────────────
    print("\n[3] Simulating expired token (exp in the past)...")
    expired = make_token(private_key, sensor_data, expires_in_minutes=-1)
    try:
        verify_token(expired, public_key)
        print("    Verified (unexpected!)")
    except jwt.ExpiredSignatureError:
        print("    Correctly rejected: ExpiredSignatureError")

    # ── Simulate tampered token ───────────────────────────────────
    print("\n[4] Simulating tampered token (payload modified)...")
    parts = token.split(".")
    tampered = parts[0] + "." + "dGFtcGVyZWQ" + "." + parts[2]   # wrong payload
    try:
        verify_token(tampered, public_key)
        print("    Verified (unexpected!)")
    except jwt.InvalidSignatureError:
        print("    Correctly rejected: InvalidSignatureError")
    except jwt.DecodeError:
        print("    Correctly rejected: DecodeError (malformed token)")

    print("\n=== All JWT checks passed ===")


if __name__ == "__main__":
    main()
