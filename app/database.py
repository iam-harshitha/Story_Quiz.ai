import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Optional
import torch

class VectorDB:
    def __init__(self):
        # Initialize encoder on CPU explicitly
        self.encoder = SentenceTransformer(
            'all-MiniLM-L6-v2',
            device='cpu',
            cache_folder='./models'
        )
        self.index = None
        self.stories = []
        
    def store_story(self, text: str) -> int:
        """Store story and return its ID"""
        with torch.no_grad():  # Disable gradient tracking
            embedding = self.encoder.encode(
                text,
                convert_to_tensor=True
            ).cpu().numpy()  # Ensure numpy array on CPU
            
        embedding = np.array([embedding]).astype('float32')
        
        if self.index is None:
            self.index = faiss.IndexFlatL2(384)  # 384-dim embeddings
            
        self.index.add(embedding)
        self.stories.append(text)
        return len(self.stories) - 1
    
    def get_story(self, story_id: int) -> Optional[str]:
        """Retrieve story by ID"""
        try:
            return self.stories[story_id]
        except IndexError:
            return None