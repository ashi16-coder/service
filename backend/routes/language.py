from fastapi import APIRouter, HTTPException
import httpx, os
from dotenv import load_dotenv
from models import TranslationRequest
from logger import get_logger

load_dotenv()
log = get_logger("language")
router = APIRouter(prefix="/language", tags=["Language"])

GOOGLE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY", "")

SUPPORTED_LANGUAGES = {
    "hi": "Hindi", "ta": "Tamil", "te": "Telugu", "kn": "Kannada",
    "ml": "Malayalam", "fr": "French", "de": "German", "ja": "Japanese",
    "zh": "Chinese", "ar": "Arabic", "es": "Spanish",
}

COMMON_PHRASES = {
    "hi": [
        {"english": "Where is the hospital?", "local": "अस्पताल कहाँ है?",     "phonetic": "Aspataal kahaan hai?"},
        {"english": "Please help me.",        "local": "कृपया मेरी मदद करें।", "phonetic": "Kripaya meri madad karein."},
        {"english": "Call the police.",       "local": "पुलिस को बुलाओ।",       "phonetic": "Police ko bulao."},
    ],
    "ta": [
        {"english": "Where is the hospital?", "local": "மருத்துவமனை எங்கே?",   "phonetic": "Maruthuvamanai enge?"},
        {"english": "Please help me.",        "local": "தயவுசெய்து உதவுங்கள்.", "phonetic": "Thayavuseidhu udavungal."},
    ],
}


@router.get("/languages")
def list_languages():
    return {"supported_languages": SUPPORTED_LANGUAGES}


@router.get("/phrases/{lang_code}")
def get_phrases(lang_code: str):
    phrases = COMMON_PHRASES.get(lang_code)
    if not phrases:
        raise HTTPException(status_code=404,
            detail=f"Phrases not available for '{lang_code}'. Available: {list(COMMON_PHRASES)}")
    return {"language": SUPPORTED_LANGUAGES.get(lang_code, lang_code), "phrases": phrases}


@router.post("/translate")
async def translate(req: TranslationRequest):
    if req.target_language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400,
            detail=f"Unsupported language '{req.target_language}'. Supported: {list(SUPPORTED_LANGUAGES)}")
    if not GOOGLE_API_KEY:
        log.warning("GOOGLE_TRANSLATE_API_KEY not set — returning mock translation")
        return {"original": req.text,
                "translated": f"[Mock: '{req.text}' → {SUPPORTED_LANGUAGES[req.target_language]}]",
                "target_language": SUPPORTED_LANGUAGES[req.target_language]}
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.post(
                "https://translation.googleapis.com/language/translate/v2",
                params={"key": GOOGLE_API_KEY},
                json={"q": req.text, "target": req.target_language, "format": "text"})
        resp.raise_for_status()
        translated = resp.json()["data"]["translations"][0]["translatedText"]
        log.info("Translated text to %s", req.target_language)
        return {"original": req.text, "translated": translated,
                "target_language": SUPPORTED_LANGUAGES[req.target_language]}
    except HTTPException:
        raise
    except Exception as exc:
        log.error("Translation error: %s", exc, exc_info=True)
        raise HTTPException(status_code=502, detail="Translation service unavailable. Try again later.")
