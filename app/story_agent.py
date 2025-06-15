from langchain_groq import ChatGroq
from gtts import gTTS
import os
from typing import Dict
import time

class StoryAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model_name="llama3-70b-8192",
            api_key=os.getenv("GROQ_API_KEY")
        )
    
    def generate_story(self, genre: str) -> Dict:
        """Generate story with both text and MP3"""
        os.makedirs("audio", exist_ok=True)
        timestamp = int(time.time())
        
        # Get story from LLM
        response = self.llm.invoke(
            f"Write a 300-word {genre} creative story suitable for creating 5 quiz questions. "
            "Return ONLY the pure story text with no formatting."
        )
        story_text = response.content
        
        # Generate audio
        mp3_path = f"audio/story_{timestamp}.mp3"
        tts = gTTS(text=story_text, lang='en', slow=True)
        tts.save(mp3_path)
        
        return {
            "text": story_text,
            "audio": mp3_path
        }