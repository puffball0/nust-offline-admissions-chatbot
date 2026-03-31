# NUST Offline Admissions Chatbot
This is a fully offline chatbot designed for NUST applicants, developed as part of a hackathon. It provides instant and context-aware answers about admissions without requiring any internet connection.

## Running the Project
To run the chatbot:
1. Navigate to the project directory.
2. Double-click the `Start_Chatbot.bat` file.

Alternatively, you can run it via terminal:
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Run the command:
```bash
python app/main.py
```



## Project Structure
- **app/**: Contains the main GUI and the chatbot logic
- **data/**: Stores the FAQ knowledge base and the AI search indices
- **assests/**: Holds the NUST logo

## Overview

The NUST Offline Admissions Chatbot is designed to answer admission-related questions instantly. 

It is lightweight, can run on low-spec laptops (i5 CPU, 8GB RAM, no GPU), and is completely offline, making it highly accessible to students.


## Features
- **Offline-first**: works without internet.
- **Semantic understanding**: uses embeddings to comprehend context.
- **Fast & responsive**: optimized vector search ensures instant answers.
- **Lightweight GUI**: built with `tkinter`, simple but user-friendly.
- **Safe & reliable**: fallback answers prevent irrelevant responses.


# Technology & How It Works

This chatbot is built entirely in Python and combines modern NLP techniques with a lightweight offline vector search to answer questions instantly and accurately.

### Knowledge Base
All the information comes from a single, structured dataset stored in `data/qa.json`. It contains curated question-answer pairs from official NUST faq site

### Understanding Questions (NLP / Embeddings)
The chatbot uses **sentence-transformers** (`all-MiniLM-L6-v2`) to turn each question into a mathematical vector. This allows it to understand the meaning behind questions, not just the words.

### Searching for Answers (Vector Database)
The chatbot uses **FAISS** to store these vectors and quickly find the closest match to the question. `data/datapreprocessing.py` converts all the Q&A data into vectors and builds a fast-searchable index, stored as `data/faq.faiss` with metadata in `data/faq_metadata.pkl`.

### Backend Engine
The engine logic resides in `app/chatbot.py`. When question is typed:
1. The engine converts the question into a vector
2. It searches the FAISS index for the most similar existing question
3. Returns the corresponding answer instantly
4. If your question is completely unrelated, it triggers a fallback response to avoid confusing answers

### Frontend / GUI
The chatbot’s interface is built with **Tkinter** and is located in `app/main.py`. It’s lightweight and fully responsive.
