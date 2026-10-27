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
# import os
# from pathlib import Path

# from dotenv import load_dotenv
# from groq import Groq

# ROOT = Path(__file__).resolve().parent.parent
# load_dotenv(ROOT / ".env", override=True)


# def get_api_key():
#     return os.getenv("GROQ_API_KEY", "").strip()


# def explain_topic(topic, question, level="Beginner",
#                   task="Explain", api_key=None):
#     key = (api_key or get_api_key()).strip()

#     if not key:
#         return (
#             "Groq API key not found.\n\n"
#             "Check that your .env file is in the main project folder "
#             "and contains GROQ_API_KEY=your_key."
#         )

#     task_instructions = {
#         "Explain": (
#             "Explain the topic step by step using simple English "
#             "and a real-world example."
#         ),
#         "Give examples": (
#             "Give at least three practical examples and explain "
#             "how each one works."
#         ),
#         "Interview preparation": (
#             "Give an interview-ready answer, important points, "
#             "a simple example, and three likely follow-up questions."
#         ),
#         "Give practice questions": (
#             "Create five practice questions with answers and "
#             "short explanations."
#         ),
#         "Give notes": (
#             "Create organized study notes with headings, definitions, "
#             "key points, examples, and a short summary."
#         )
#     }

#     prompt = f"""
# You are AI Study Mentor, a patient and encouraging tutor.

# Subject: {topic}
# Student's question: {question}
# Student's level: {level}

# Task:
# {task_instructions.get(task, task_instructions["Explain"])}

# Instructions:
# - Use clear, simple English suitable for the student's level.
# - Use headings and bullet points where helpful.
# - Explain technical terms before using them.
# - Include code examples when relevant.
# - Explain what the example does.
# - Be accurate and avoid unnecessary complexity.
# """

#     try:
#         client = Groq(api_key=key)

#         response = client.chat.completions.create(
#             model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         "You are a friendly, accurate AI tutor. "
#                         "Help students understand concepts, not just "
#                         "memorize answers."
#                     )
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=0.5,
#             max_tokens=1500
#         )

#         answer = response.choices[0].message.content
#         return answer or "No answer was returned. Please try again."

#     except Exception as error:
#         message = str(error)
#         lower_message = message.lower()

#         if "401" in message or "authentication" in lower_message:
#             return (
#                 "### Groq authentication failed\n"
#                 "Check your GROQ_API_KEY in the .env file. "
#                 "Make sure it is the secret key, not the tracking ID."
#             )

#         if "429" in message or "rate_limit" in lower_message:
#             return (
#                 "### Groq usage limit reached\n"
#                 "You may have reached the free-tier request or token limit. "
#                 "Check your Groq console and try again when the limit resets."
#             )

#         if "model" in lower_message and (
#             "not found" in lower_message
#             or "decommissioned" in lower_message
#         ):
#             return (
#                 "### Model unavailable\n"
#                 "The selected Groq model may no longer be available. "
#                 "Check the models listed in your Groq console and update "
#                 "GROQ_MODEL in your .env file."
#             )

#         return (
#             "### Unable to generate an answer\n"
#             "Please check your internet connection and Groq API settings.\n\n"
#             f"Technical details: {message}"
#         )


# def make_study_plan(subject, days=7, hours=2):
#     days = max(1, min(int(days), 30))
#     hours = max(1, min(int(hours), 12))

#     topics = [
#         "Learn the fundamentals",
#         "Understand key terms and definitions",
#         "Study simple examples",
#         "Practice the main concepts",
#         "Learn intermediate concepts",
#         "Solve exercises and revise",
#         "Take a practice test and review mistakes"
#     ]

#     lines = [
#         f"# {subject} — {days}-Day Study Plan",
#         "",
#         f"**Daily study time:** {hours} hour(s)",
#         ""
#     ]

#     for day in range(1, days + 1):
#         topic = topics[(day - 1) % len(topics)]

#         lines.extend([
#             f"## Day {day}: {topic}",
#             f"- Study {subject}: {topic.lower()}.",
#             f"- Spend {hours} hour(s) learning and practicing.",
#             "- Write short notes in your own words.",
#             "- Review what you learned before finishing.",
#             ""
#         ])

#     lines.extend([
#         "## Tips for success",
#         "- Study consistently.",
#         "- Practice instead of only reading.",
#         "- Revise difficult concepts.",
#         "- Take breaks when needed."
#     ])

#     return "\n".join(lines)
