
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="ScamShield API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScanRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "ScamShield backend is running!"}


@app.post("/check")
def check_message(request: ScanRequest):
    text = request.message.lower().strip()

    if not text:
        return {
            "verdict": "SUSPICIOUS",
            "reasons": ["Please enter a message."]
        }

    fake_phrases = [
        "send otp",
        "send your otp",
        "share your otp",
        "won a prize",
        "claim your reward",
        "claim your prize",
        "account will be blocked",
        "pay registration fee",
        "free money",
        "pay ₹100 to get scholarship",
        "pay 100 to get scholarship",
        "send password",
        "share your password",
        "send otp immediately",
        "your bank account will be blocked",
        "account suspended",
        "update your bank details",
        "click here to claim",
        "pay processing fee",
        "pay to receive your prize",
        "share your bank details",
        "verify your account immediately",
        "send money to unlock",
        "guaranteed job",
        "investment guaranteed returns"
    ]

    suspicious_phrases = [
        "verify your kyc",
        "urgent",
        "click this link",
        "limited time",
        "scholarship approved"
    ]

    reasons = []

    for phrase in fake_phrases:
        if phrase in text:
            reasons.append(
                f"High-risk phrase detected: {phrase}"
            )

    for phrase in suspicious_phrases:
        if phrase in text:
            reasons.append(
                f"Warning phrase detected: {phrase}"
            )

    if any(phrase in text for phrase in fake_phrases):
        verdict = "FAKE"
    elif reasons:
        verdict = "SUSPICIOUS"
    else:
        verdict = "NEEDS VERIFICATION"
        reasons.append(
            "No listed warning phrases detected. "
            "This does not guarantee the message is safe."
        )

    return {
        "verdict": verdict,
        "reasons": reasons
    }




from urllib.parse import urlparse
import ipaddress


class URLRequest(BaseModel):
    url: str


@app.post("/check-url")
def check_url(request: URLRequest):
    url = request.url.strip()

    if not url:
        return {
            "verdict": "SUSPICIOUS",
            "reasons": ["Please enter a website URL."]
        }

    if "://" not in url:
        url = "https://" + url

    parsed = urlparse(url)
    hostname = parsed.hostname
    reasons = []

    if parsed.scheme not in ("http", "https") or not hostname:
        return {
            "verdict": "SUSPICIOUS",
            "reasons": ["Please enter a valid website URL."]
        }

    hostname = hostname.lower()

    try:
        ipaddress.ip_address(hostname)
        reasons.append(
            "This URL uses an IP address instead of a domain name."
        )
    except ValueError:
        pass

    if hostname.startswith("xn--") or ".xn--" in hostname:
        reasons.append(
            "The domain contains encoded international characters."
        )

    if len(hostname.split(".")) > 4:
        reasons.append(
            "The domain has an unusually large number of subdomains."
        )

    if parsed.scheme != "https":
        reasons.append("The URL does not use HTTPS.")

    if reasons:
        verdict = "SUSPICIOUS"
    else:
        verdict = "NEEDS VERIFICATION"
        reasons.append(
            "No basic URL warning signs were detected. "
            "This does not prove the website is safe."
        )

    return {
        "verdict": verdict,
        "reasons": reasons
    }





from urllib.parse import urlparse
import requests


class VideoRequest(BaseModel):
    video_url: str
    claim: str = ""
    language: str = "en"


@app.post("/check-video")
def check_video(request: VideoRequest):
    video_url = request.video_url.strip()
    claim = request.claim.strip()
    reasons = []

    try:
        parsed = urlparse(video_url)
        host = (parsed.hostname or "").lower()

        if host in ("youtu.be", "www.youtu.be"):
            video_id = parsed.path.strip("/")
        elif host in ("youtube.com", "www.youtube.com", "m.youtube.com"):
            if parsed.path == "/watch":
                from urllib.parse import parse_qs
                video_id = parse_qs(parsed.query).get("v", [""])[0]
            elif parsed.path.startswith(("/shorts/", "/embed/")):
                video_id = parsed.path.split("/")[2]
            else:
                video_id = ""
        else:
            video_id = ""

        if not video_id:
            return {
                "verdict": "SUSPICIOUS",
                "reasons": ["Please enter a valid YouTube video URL."]
            }

        title = ""
        try:
            response = requests.get(
                "https://www.youtube.com/oembed",
                params={
                    "url": "https://www.youtube.com/watch?v=" + video_id,
                    "format": "json"
                },
                timeout=5
            )
            if response.ok:
                title = response.json().get("title", "")
        except requests.RequestException:
            pass

        if not claim:
            return {
                "verdict": "NEEDS VERIFICATION",
                "reasons": [
                    "Enter the specific claim made in the video.",
                    "Video title: " + (title or "Could not retrieve the title.")
                ]
            }

        lower_claim = claim.lower()

        warning_phrases = [
            "pay ₹100",
            "pay 100",
            "registration fee",
            "send otp",
            "share your otp",
            "guaranteed scholarship",
            "guaranteed prize",
            "free money"
        ]

        for phrase in warning_phrases:
            if phrase in lower_claim:
                reasons.append("Warning sign detected: " + phrase)

        if any(word in claim for word in ["స్కాలర్షిప్", "డబ్బులు చెల్లించండి", "ఓటీపీ"]):
            reasons.append(
                "Telugu claim contains wording that needs careful verification."
            )

        return {
            "verdict": "SUSPICIOUS" if reasons else "NEEDS VERIFICATION",
            "reasons": reasons or [
                "No configured warning phrases detected. This does not prove the claim is true."
            ],
            "video_title": title
        }

    except Exception:
        return {
            "verdict": "NEEDS VERIFICATION",
            "reasons": ["Could not fully check this video. Verify the claim using an official source."]
        }

