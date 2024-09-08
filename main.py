from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import edge_tts
import tempfile
import asyncio
from typing import List, Optional
from fastapi.responses import FileResponse

app = FastAPI()

# Define a request model for TTS
class TextToSpeechRequest(BaseModel):
    text: str
    voice: str
    rate: Optional[int] = None  # Optional parameter for rate
    pitch: Optional[int] = None  # Optional parameter for pitch

# Get all available voices
async def get_voices():
    voices = await edge_tts.list_voices()
    return [
        {"name": f"{v['ShortName']} - {v['Locale']} ({v['Gender']})", "short_name": v['ShortName']}
        for v in voices
    ]

# Text-to-speech function
async def text_to_speech(text: str, voice: str, rate: Optional[int], pitch: Optional[int]) -> str:
    if not text.strip():
        raise HTTPException(status_code=400, detail="Please enter text to convert.")
    if not voice:
        raise HTTPException(status_code=400, detail="Please select a voice.")
    
    voice_short_name = voice.split(" - ")[0]
    
    # Only include rate and pitch if they are provided
    kwargs = {}
    if rate is not None:
        kwargs['rate'] = f"{rate:+d}%"
    if pitch is not None:
        kwargs['pitch'] = f"{pitch:+d}Hz"
    
    communicate = edge_tts.Communicate(text, voice_short_name, **kwargs)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_path = tmp_file.name
        await communicate.save(tmp_path)
    return tmp_path

@app.post("/tts")
async def generate_speech(request: TextToSpeechRequest):
    text = request.text
    voice = request.voice
    rate = request.rate
    pitch = request.pitch

    try:
        # Generate speech
        audio_path = await text_to_speech(text, voice, rate, pitch)
        
        # Return the audio file as a response
        return FileResponse(audio_path, media_type="audio/mpeg", filename="output.mp3")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/voices")
async def get_available_voices(query: Optional[str] = Query(None, description="Filter voices by name or locale")):
    try:
        voices = await get_voices()
        
        if query:
            # Filter voices based on query
            filtered_voices = [voice for voice in voices if query.lower() in voice['name'].lower()]
        else:
            filtered_voices = voices

        return {"voices": filtered_voices}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Uvicorn server entry point - Uncomment if running locally
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
