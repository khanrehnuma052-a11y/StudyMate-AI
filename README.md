# StudyMate AI

## About
StudyMate AI is a simple AI-powered study assistant that helps students understand topics, summarize notes, generate quizzes, and ask study questions.

## Features
- AI topic explanation
- Note summarization
- Quiz generation
- AI study questions
- Responsive UI

## Technology
- Python
- Flask
- HTML
- CSS
- JavaScript
- Google Gemini API

## How to Run
Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` in the project root:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run the app:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Project Architecture

```text
Browser
   ↓
JavaScript
   ↓
Flask
   ↓
Gemini API
   ↓
Flask
   ↓
Browser
```

The Gemini API key is loaded by Flask from `.env` and is never sent to the browser.
