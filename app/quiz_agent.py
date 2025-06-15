from langchain_groq import ChatGroq
import os
from typing import List, Dict
import random

class QuizAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model_name="llama3-70b-8192",
            api_key=os.getenv("GROQ_API_KEY")
        )
    
    def generate_quiz(self, story_text: str) -> List[Dict]:
        """Generate 5 MCQs with shuffled options"""
        response = self.llm.invoke(
            f"Create 5 multiple choice questions about this story:\n{story_text}\n"
            "Format each EXACTLY like:\n"
            "Q: question\n"
            "A: correct answer\n"
            "W1: wrong option 1\n"
            "W2: wrong option 2\n"
            "W3: wrong option 3\n"
            "Separate questions with '---'"
        )
        
        questions = []
        for q_block in response.content.split("---"):
            question_data = {}
            options = []
            
            for line in q_block.strip().split("\n"):
                if line.startswith("Q:"):
                    question_data["question"] = line[3:].strip()
                elif line.startswith("A:"):
                    correct_answer = line[3:].strip()
                    options.append(correct_answer)
                elif line.startswith("W"):
                    options.append(line[4:].strip())
            
            if len(options) == 4:  # 1 correct + 3 wrong answers
                random.shuffle(options)
                question_data["options"] = options
                question_data["correct_idx"] = options.index(correct_answer)
                questions.append(question_data)
        
        return questions[:5]  # Return max 5 questions