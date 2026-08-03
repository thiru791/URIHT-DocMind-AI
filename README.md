# URIHT DocMind AI

URIHT DocMind AI is a web application for working with PDF documents using natural language.

A user can upload a PDF, extract its text, generate a summary, and ask questions about the uploaded document. The application uses a React frontend, a FastAPI backend, and Google Gemini for document-based responses.

## Features

- PDF upload through the web interface
- Text extraction from PDF documents
- Automatic document summary
- Question answering based on uploaded document content
- Relevant document sections are selected before sending context to the AI
- Separate frontend and backend applications
- Responsive interface
- Local development and cloud deployment support

## How it works

The application follows a simple flow:

1. A PDF is uploaded from the frontend.
2. The backend extracts the text from the document.
3. The extracted text is divided into smaller sections.
4. The sections are stored for document search.
5. When the user asks a question, the backend finds relevant sections from the document.
6. The selected content is sent to Google Gemini along with the user's question.
7. The generated response is returned to the frontend.

## Project structure

```text
URIHT-DocMind-AI/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py
│   │   ├── db/
│   │   ├── models/
│   │   ├── services/
│   │   │   ├── ai_service.py
│   │   │   ├── embedding_service.py
│   │   │   ├── pdf_service.py
│   │   │   └── chat_service.py
│   │   └── uploads/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── styles/
│   ├── package.json
│   └── vite.config.js
│
├── screenshots/
│
├── .gitignore
└── README.md
