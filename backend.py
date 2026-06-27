from dotenv import load_dotenv
from anthropic import Anthropic
from fastapi import FastAPI
from pydantic import BaseModel
from duckduckgo_search import DDGS
import os

app = FastAPI()

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


@app.get("/")
def home():
    return {"message": "welcome to gen ai"}


def search_web(query: str, max_results: int = 6) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results, timelimit="d"))  # "d" = last 1 day
        if not results:
            # fallback: no time limit
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
        if not results:
            return None
        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(
                f"[Result {i}]\nTitle: {r.get('title', '')}\nSummary: {r.get('body', '')}\nURL: {r.get('href', '')}"
            )
        return "\n\n".join(formatted)
    except Exception as e:
        print(f"Search error: {e}")
        return None


class QuestionRequest(BaseModel):
    userQuestion: str


@app.post("/ask-ai")
def requestQuestion(request: QuestionRequest):
    web_results = search_web(request.userQuestion)

    if web_results:
        system_prompt = (
            "You are a real-time AI assistant. You have been given live web search results fetched right now. "
            "These results are current and up to date as of today. "
            "ALWAYS answer using these search results. Do NOT say 'as of my knowledge cutoff' or mention any cutoff date. "
            "Do NOT say you don't have access to current data — you do, via the search results provided. "
            "Answer directly and confidently using the search results. "
            "Respond in plain text only: no markdown, no headers, no bold, no bullet points, no emojis. "
            "Plain sentences and paragraphs only."
        )
        user_message = (
            f"Live web search results (fetched right now):\n\n{web_results}\n\n"
            f"Question: {request.userQuestion}\n\n"
            "Answer using the search results above. Give the most current information available."
        )
    else:
        system_prompt = (
            "You are a helpful assistant. Answer the user's question clearly and accurately. "
            "Respond in plain text only: no markdown, no headers, no bold, no bullet points, no emojis."
        )
        user_message = request.userQuestion

    response = client.messages.create(
        model="claude-sonnet-4-6",
        messages=[{"role": "user", "content": user_message}],
        system=system_prompt,
        temperature=0.2,
        max_tokens=700,
    )

    return {
        "answer": response.content[0].text,
        "web_search_used": web_results is not None
    }
