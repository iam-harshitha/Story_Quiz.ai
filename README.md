# Story_Quiz

Story_Quiz.ai is a creative and educational AI application that turns generated stories into interactive audio-based quizzes. Leveraging the power of **Groq LLMs, gTTS, Langchain and Sentence Transformers,** this app creates personalized stories in your chosen genre, narrates them aloud, and generates comprehension quizzes to test your understanding — all within a sleek, colorful Streamlit interface.

---

🚀 How It Works

### 📜 Step 1: Generate a Story
- User selects a story genre (Fantasy, Sci-Fi, or Mystery).
- Groq LLM (LLaMA 3) generates a unique ~300-word creative story.
- The story is saved as both text and a spoken MP3 audio file using gTTS.

### 🎧 Step 2: Listen and Comprehend
- Users can listen to the narrated story directly in the browser using Streamlit's audio component. 

### 🧩 Step 3: Take the Quiz
- The app uses the story as context to generate 5 multiple-choice questions (MCQs).
- Users answer the questions, and upon submission:
   1. Immediate feedback is shown with color-coded indicators.
   2. A final score out of 5 is displayed with dynamic visual effects.

---

## 🛠️ Tech Stack & Purpose

| Technology          | Role                                                                 |
|---------------------|----------------------------------------------------------------------|
| Streamlit           | 🎨 Interactive UI with genre selection, audio player & quizzes
| gTTS                | 🎤 Text-to-speech for MP3 generation of the story                               |
| SentenceTransformers| 🧩 Embedding stories for vector DB (for future extensions)                                  |
| Groq API            | 🧠 Story and quiz generation via fast LLM inference                            |
| FAISS              | 📚 Efficient vector search (used in database.py)                             |
| Python + dotenv      | 🐍 Core logic and environment management                               |

---

## 🧰 Source Files

| File                  | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `main.py`              | 🚀 Streamlit UI logic for story generation and quiz display       |
| `story_agent.py` | Uses Groq LLM + gTTS to create and narrate stories|
| `quiz_agent.py` | Uses Groq LLM to turn stories into 5 MCQ questions |
| `database.py` | Embeds and stores stories using FAISS for indexing |
| `requirements.txt`    | 📦 Python dependencies                |
| `audio/`                |   Stores generated audio stories as MP3 files                           |

---

## 🖼️ System Architecture
![Screenshot 2025-06-15 162447](https://github.com/user-attachments/assets/3470c0fd-5fbd-4881-813a-be915e1c9804)

---

## 📸 Screenshots

![Screenshot 2025-06-15 152117](https://github.com/user-attachments/assets/01cd7d59-6423-4e4a-a01f-d41366ac684b)
 
![Screenshot 2025-06-15 152152](https://github.com/user-attachments/assets/1f19e3c1-5cb2-4c52-9f4d-6d1f351803f4)

![Screenshot 2025-06-15 152215](https://github.com/user-attachments/assets/e631c528-ee50-44fb-8b55-9ee31c784743)
  
![Screenshot 2025-06-15 152234](https://github.com/user-attachments/assets/a9aff3dd-dad2-46cf-b9c7-f003d51ee914)

  
---

## 🔮 Future Improvements

- 🎙️ Voice input for answering quizzes
- 📚 Save quiz scores and generate user profiles
- 🧠 Add memory-based story personalization
- 🔎 Add story recommendation based on previous interactions
- 🌐 Multi-language story support using TTS engines

