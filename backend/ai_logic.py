import os
import json
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env", override=True)


def get_api_key():
    return os.getenv("GROQ_API_KEY", "").strip()


def get_model():
    return os.getenv("GROQ_MODEL", "openai/gpt-oss-120b").strip()


def explain_topic(topic, question, level="Beginner",
                  task="Explain", api_key=None):
    key = api_key or get_api_key()

    if not key:
        return "Groq API key not found. Please check your .env file."

    try:
        client = Groq(api_key=key)

        response = client.chat.completions.create(
            model=get_model(),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly AI study mentor. "
                        "Explain concepts clearly using simple language, "
                        "examples, and practical applications."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Subject: {topic}\n"
                        f"Level: {level}\n"
                        f"Help needed: {task}\n"
                        f"Question: {question}\n\n"
                        "Give a clear, well-organized answer."
                    )
                }
            ],
            temperature=0.5,
            max_tokens=1800
        )

        return response.choices[0].message.content or (
            "Sorry, no answer was returned. Please try again."
        )

    except Exception as e:
        return f"Unable to generate an answer. Please check your Groq settings.\n\nDetails: {e}"


def make_study_plan(subject, days=7, hours=2):
    key = get_api_key()

    if not key:
        return "Groq API key not found. Please check your .env file."

    try:
        client = Groq(api_key=key)

        response = client.chat.completions.create(
            model=get_model(),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a study planner. Create practical "
                        "study plans with daily topics, practice, "
                        "and revision."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Create a {days}-day study plan for {subject}. "
                        f"The learner can study {hours} hours per day. "
                        "Use a day-by-day Markdown table. Include "
                        "learning, hands-on practice, and revision."
                    )
                }
            ],
            temperature=0.5,
            max_tokens=2500
        )

        return response.choices[0].message.content or (
            "Sorry, no study plan was returned."
        )

    except Exception as e:
        return f"Unable to create the study plan. Please check your Groq settings.\n\nDetails: {e}"


def generate_quiz(subject, count=10, level="Beginner"):
    key = get_api_key()

    if not key:
        raise ValueError(
            "Groq API key not found. Please check your .env file."
        )

    count = max(5, min(int(count), 15))

    client = Groq(api_key=key)

    prompt = f"""
Create exactly {count} multiple-choice quiz questions.

Subject: {subject}
Difficulty: {level}

Requirements:
- Make questions educational and factually accurate.
- Use different concepts and avoid repeating questions.
- Give exactly four answer options per question.
- Only one option must be correct.
- Keep explanations simple and useful.
- Do not reveal the correct answer in the question.
- Return valid JSON only, with no Markdown fences.

Use this exact JSON structure:
{{
  "questions": [
    {{
      "question": "Question text",
      "options": [
        "First option",
        "Second option",
        "Third option",
        "Fourth option"
      ],
      "answer": "Exact text of the correct option",
      "explanation": "Short explanation of why the answer is correct"
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {
                "role": "system",
                "content": (
                    "You generate accurate educational quizzes. "
                    "Return only valid JSON matching the requested structure."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=6000
    )

    content = response.choices[0].message.content or ""
    content = content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "", 1)
        content = content.replace("```", "").strip()

    data = json.loads(content)
    questions = data.get("questions", [])

    if len(questions) != count:
        raise ValueError(
            f"The AI returned {len(questions)} questions instead of "
            f"{count}. Please generate the quiz again."
        )

    validated = []

    for item in questions:
        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        answer = str(item.get("answer", "")).strip()
        explanation = str(item.get("explanation", "")).strip()

        if (
            not question
            or not isinstance(options, list)
            or len(options) != 4
            or any(not isinstance(option, str) or not option.strip()
                   for option in options)
            or answer not in options
            or not explanation
        ):
            raise ValueError(
                "The AI returned an invalid question. Please try again."
            )

        validated.append({
            "q": question,
            "options": options,
            "answer": answer,
            "why": explanation
        })

    return validated
