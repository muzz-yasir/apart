from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Literal
import uuid
import hashlib
import json
from datetime import datetime, timedelta
import random
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
import math
import requests
import statistics

app = FastAPI()

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def calculate_human_score(content):
    # Tokenize the content
    tokens = word_tokenize(content.lower())
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Calculate lexical diversity
    lexical_diversity = len(set(tokens)) / len(tokens) if tokens else 0
    
    # Calculate sentence length variation
    sentences = sent_tokenize(content)
    sentence_lengths = [len(word_tokenize(sentence)) for sentence in sentences if sentence.strip()]
    sentence_length_variation = statistics.stdev(sentence_lengths) if len(sentence_lengths) > 1 else 0
    
    # Check for overused words or phrases (common in AI-generated text)
    word_freq = Counter(tokens)
    overused_words = sum(1 for word, count in word_freq.items() if count > len(tokens) * 0.1)
    
    # Calculate final score (adjust weights as needed)
    score = (
        0.4 * lexical_diversity +
        0.3 * min(sentence_length_variation / 5, 1) +
        0.3 * (1 - overused_words / len(set(tokens)) if set(tokens) else 0)
    )
    
    return min(max(score, 0), 1)  # Ensure score is between 0 and 1

# Blockchain implementation
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, str(datetime.now()), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), str(datetime.now()), data, previous_block.hash)
        self.chain.append(new_block)
        return new_block.hash

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

# Initialize blockchain
blockchain = Blockchain()

# In-memory storage for posts and creators
posts = []
creators = []

# Pydantic models
class ContentVerificationRequest(BaseModel):
    content: str
    type: Literal["text", "image", "video"]
    metadata: Dict

class CreatorVerificationRequest(BaseModel):
    username: str
    email: str
    metadata: Dict

@app.post("/v1/verify")
async def verify_content(request: ContentVerificationRequest):
    verification_id = str(uuid.uuid4())
    
    if request.type == "text":
        human_score = calculate_human_score(request.content)
    else:
        # For non-text content, use a placeholder score
        # In a real system, you'd implement specific verification for images, videos, etc.
        human_score = 0.5
    
    transaction_data = {
        "verification_id": verification_id,
        "content_hash": hashlib.sha256(request.content.encode()).hexdigest(),
        "human_score": human_score,
        "timestamp": str(datetime.now())
    }
    block_hash = blockchain.add_block(transaction_data)
    
    post = {
        "id": verification_id,
        "title": request.metadata.get("title", "Untitled"),
        "content": request.content,
        "author": request.metadata.get("author", "Anonymous"),
        "human_score": human_score,
        "blockchain_hash": block_hash,
        "timestamp": str(datetime.now())
    }
    posts.append(post)
    
    return {
        "verification_id": verification_id,
        "human_score": human_score,
        "ai_probability": 1 - human_score,
        "certification_token": f"HCVS-{random.randint(1000000, 9999999)}",
        "blockchain_hash": block_hash,
        "timestamp": str(datetime.now())
    }

@app.get("/v1/posts")
async def get_posts():
    return posts

@app.get("/v1/creators")
async def get_creators():
    return creators

@app.get("/v1/blockchain/explore")
async def explore_blockchain():
    return {
        "chain_length": len(blockchain.chain),
        "last_block_hash": blockchain.get_latest_block().hash,
        "is_valid": blockchain.is_chain_valid(),
        "blocks": [
            {
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "hash": block.hash,
                "previous_hash": block.previous_hash
            }
            for block in blockchain.chain
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)