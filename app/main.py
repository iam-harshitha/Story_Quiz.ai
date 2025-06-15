import streamlit as st
from story_agent import StoryAgent
from quiz_agent import QuizAgent
from dotenv import load_dotenv
import random

load_dotenv()

# Custom CSS for colorful UI
st.markdown("""
<style>
    :root {
        --primary: #6a11cb;
        --secondary: #2575fc;
        --accent: #ff7e5f;
        --light: #f8f9fa;
        --success: #28a745;
        --warning: #fd7e14;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--light) 0%, #e9ecef 100%);
    }
    
    .title-box {
        background: linear-gradient(to right, var(--primary), var(--secondary));
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .quiz-box {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 5px solid var(--accent);
    }
    
    .correct-answer {
        background-color: #d4edda !important;
        color: #155724 !important;
        border-left: 4px solid var(--success) !important;
    }
    
    .wrong-answer {
        background-color: #f8d7da !important;
        color: #721c24 !important;
        border-left: 4px solid #dc3545 !important;
    }
    
    .score-display {
        font-size: 1.5rem;
        font-weight: bold;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    
    .good-score {
        background: linear-gradient(to right, #38ef7d, #11998e);
        color: white;
    }
    
    .bad-score {
        background: linear-gradient(to right, #f46b45, #eea849);
        color: white;
    }
    
    .stButton>button {
        background: linear-gradient(to right, var(--primary), var(--secondary));
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
     /* Genre Selector Styling */
    .stSelectbox > div > div {
        font-size: 1.2rem !important;
        color: #6a11cb !important;
        font-weight: 500 !important;
    }
    
    .stSelectbox > label {
        font-size: 1.3rem !important;
        color: #2575fc !important;
        font-weight: 600 !important;
        margin-bottom: 8px !important;
    }
    
    /* Options in Dropdown */
    .st-ae {
        font-size: 1.1rem !important;
    }
    
    /* Match headline gradient */
    .genre-headline {
        background: linear-gradient(to right, #6a11cb, #2575fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize agents
story_agent = StoryAgent()
quiz_agent = QuizAgent()

# Initialize session state
if 'story_data' not in st.session_state:
    st.session_state.story_data = None
if 'quiz' not in st.session_state:
    st.session_state.quiz = None
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = [None] * 5
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'score' not in st.session_state:
    st.session_state.score = 0

# --- UI Components ---
st.markdown('<div class="title-box"><h1 style="margin:0; text-align:center">🎧 Story Quizmaster</h1></div>', unsafe_allow_html=True)

# Genre selection with colorful cards
st.markdown('<div class="genre-headline">Choose Your Story Genre</div>', unsafe_allow_html=True)
genre = st.selectbox(
    "",
    ["Fantasy", "Sci-Fi", "Mystery"],
    help="Select a genre for your personalized story",
    label_visibility="collapsed"
)

# Story Generation
if st.button("✨ Generate Story", key="gen_story"):
    with st.spinner("Weaving your magical story..."):
        try:
            story_data = story_agent.generate_story(genre)
            st.session_state.story_data = story_data
            st.session_state.quiz = None
            st.session_state.user_answers = [None] * 5
            st.session_state.show_results = False
            st.session_state.score = 0
            st.success("Your story is ready! 🎉")
        except Exception as e:
            st.error(f"🔮 The story crystal ball broke! Please try again. Error: {str(e)}")

# Persistent Audio Player with style
if st.session_state.story_data and st.session_state.story_data.get("audio"):
    st.markdown("### 🎧 Story Audio")
    st.audio(st.session_state.story_data["audio"], format="audio/mp3")

# Quiz Generation
if st.session_state.story_data and not st.session_state.quiz:
    if st.button("🧩 Generate Quiz", key="gen_quiz"):
        with st.spinner("Crafting challenging questions..."):
            try:
                st.session_state.quiz = quiz_agent.generate_quiz(
                    st.session_state.story_data["text"]
                )
                st.success("Quiz generated! Test your knowledge 💡")
            except Exception as e:
                st.error(f"❌ Failed to generate quiz: {str(e)}")

# Quiz Display with colorful elements
if st.session_state.quiz:
    st.markdown('<div class="title-box"><h2 style="margin:0">🧠 Story Quiz</h2></div>', unsafe_allow_html=True)
    
    for i, q in enumerate(st.session_state.quiz):
        options = q["options"]
        correct_idx = q["correct_idx"]
        user_answer = st.session_state.user_answers[i]
        
        with st.container():
            st.markdown(f'<div class="quiz-box"><h4>Q{i+1}: {q["question"]}</h4>', unsafe_allow_html=True)
            
            if st.session_state.show_results:
                # Show results with color feedback
                for j, option in enumerate(options):
                    is_correct = (j == correct_idx)
                    is_user_choice = (option == user_answer)
                    
                    if is_user_choice and is_correct:
                        st.markdown(f"""
                        <div class="correct-answer" style="padding:10px; margin:5px 0; border-radius:5px;">
                            ✅ {option}
                        </div>
                        """, unsafe_allow_html=True)
                    elif is_user_choice and not is_correct:
                        st.markdown(f"""
                        <div class="wrong-answer" style="padding:10px; margin:5px 0; border-radius:5px;">
                            ❌ {option}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="padding:10px; margin:5px 0; border-radius:5px;">
                            {option}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                # Interactive quiz
                st.session_state.user_answers[i] = st.radio(
                    f"Select an answer:",
                    options,
                    index=None,
                    key=f"q_{i}",
                    label_visibility="collapsed"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)

    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if not st.session_state.show_results and st.button("📩 Submit Answers", key="submit"):
            # Calculate score
            st.session_state.score = sum(
                1 for i, q in enumerate(st.session_state.quiz)
                if st.session_state.user_answers[i] == q["options"][q["correct_idx"]]
            )
            st.session_state.show_results = True
            st.rerun()
    
    with col2:
        if st.session_state.show_results and st.button("🔄 Try Again", key="retry"):
            st.session_state.user_answers = [None] * 5
            st.session_state.show_results = False
            st.session_state.score = 0
            st.rerun()

# Results Display with celebration
if st.session_state.show_results:
    if st.session_state.score >= 3:
        st.markdown(f"""
        <div class="score-display good-score">
            🎉 Your Score: {st.session_state.score}/5 🎉
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
        st.success("Excellent work! You're a story master!")
    else:
        st.markdown(f"""
        <div class="score-display bad-score">
            😟 Your Score: {st.session_state.score}/5
        </div>
        """, unsafe_allow_html=True)
        st.warning("Listen to the story again and try one more time!")
        