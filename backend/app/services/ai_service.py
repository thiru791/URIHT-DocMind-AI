import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

print("=" * 50)
print("Current directory:", os.getcwd())
print("API KEY:", os.getenv("GOOGLE_API_KEY"))
print("=" * 50)

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def generate_summary(text: str):

    prompt = f"""
You are Uriht DocMind AI.

Analyze the following document.

Return:

# Executive Summary

# Key Points

# Important Dates

# Important People

# Important Numbers

# Action Items

# Final Conclusion

Document:

{text}
"""

    response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt,
)

    return response.text
def answer_question(question, context):

    prompt = f"""
You are DocMind AI.

Answer ONLY from the document below.

If the answer is not present,
reply:

"I couldn't find that information in the document."

Document:

{context}

Question:

{question}
"""

    response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt,
)
    return response.text