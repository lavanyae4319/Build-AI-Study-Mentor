import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from backend.ai_logic import (
    explain_topic,
    get_api_key,
    make_study_plan,
    generate_quiz
)

st.set_page_config(
    page_title="AI Study Mentor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- DESIGN ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: #0b1020;
    color: #f3f5ff;
}
[data-testid="stHeader"] {
    background: rgba(11,16,32,0.95);
}
[data-testid="stSidebar"] {
    background: #11182b;
    border-right: 1px solid #27314b;
}
[data-testid="stSidebar"] * {
    color: #edf0ff;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}
.hero {
    background: linear-gradient(120deg, #242e60, #512f80 55%, #173b69);
    padding: 32px;
    border-radius: 22px;
    border: 1px solid #55528e;
    margin-bottom: 25px;
}
.hero h1 {
    color: white;
    font-size: 36px;
    font-weight: 800;
    margin: 0 0 10px 0;
}
.hero p {
    color: #e0e5ff;
    font-size: 16px;
    margin-bottom: 0;
}
.section-title {
    font-size: 23px;
    font-weight: 750;
    color: #f4f6ff;
    margin: 18px 0 12px 0;
}
.info-card {
    background: #151e33;
    border: 1px solid #2b3857;
    padding: 22px;
    border-radius: 17px;
    min-height: 145px;
    margin-bottom: 12px;
}
.info-card h3 {
    font-size: 17px;
    color: #c8d0ff;
    margin: 8px 0;
}
.info-card p {
    font-size: 14px;
    color: #b8c3dc;
    line-height: 1.6;
}
.big-icon {
    font-size: 27px;
}
.small-label {
    color: #aebcdb;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}
div[data-testid="stMetric"] {
    background: #151e33;
    border: 1px solid #2b3857;
    padding: 17px;
    border-radius: 15px;
}
div[data-testid="stMetricLabel"] {
    color: #c2cce5;
}
div[data-testid="stMetricValue"] {
    color: #ffffff;
}
.stButton > button, .stDownloadButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(90deg, #7657f6, #5b7cfa);
    color: white;
    border: 0;
    border-radius: 10px;
    min-height: 44px;
    font-weight: 700;
    width: 100%;
}
.stButton > button:hover, .stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(90deg, #6040df, #4265e8);
    color: white;
    border: 0;
}
.stTextInput input, .stTextArea textarea {
    background: #121b2f;
    color: #ffffff;
    border: 1px solid #354565;
    border-radius: 10px;
}
.stSelectbox div[data-baseweb="select"] > div {
    background: #121b2f;
    color: white;
    border-color: #354565;
}
.stRadio label, .stCheckbox label {
    color: #e8ecfa !important;
}
hr {
    border-color: #2b3857;
}
div[data-testid="stAlert"] {
    border-radius: 12px;
}
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION DATA ----------
defaults = {
    "completed_quizzes": 0,
    "best_score": 0,
    "questions_asked": 0,
    "quiz_result": None,
    "quiz_questions": [],
    "quiz_subject": "Python",
    "quiz_level": "Beginner",
    "quiz_count": 5
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

api_key = get_api_key()

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 🎓 Study Mentor")
    st.caption("YOUR PERSONAL AI LEARNING SPACE")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "🤖 Study Assistant",
            "📅 Study Planner",
            "🧠 Quick Quiz",
            "📈 My Progress"
        ]
    )

    st.divider()

    if api_key:
        st.success("Groq key detected")
    else:
        st.error("Groq key not found")

    st.caption("Learn a little every day. Improve one step at a time.")
    st.markdown("---")
    st.caption("AI Study Mentor · Build Sprint Project")

# ---------- DASHBOARD ----------
if page == "🏠 Dashboard":
    st.markdown("""
    <div class="hero">
        <div class="small-label">WELCOME TO YOUR LEARNING SPACE</div>
        <h1>Learn smarter. Grow faster. 🚀</h1>
        <p>Your personal study companion for explanations, interview preparation,
        study planning, and quick practice.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Your learning overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Questions asked", st.session_state.questions_asked)
    col2.metric("Quizzes completed", st.session_state.completed_quizzes)
    col3.metric("Best quiz score", f"{st.session_state.best_score}%")

    st.markdown(
        '<div class="section-title">What would you like to do?</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="info-card">
            <div class="big-icon">🤖</div>
            <h3>AI Study Assistant</h3>
            <p>Understand difficult topics with simple explanations,
            real-world examples, notes, and interview answers.</p>
        </div>
        <div class="info-card">
            <div class="big-icon">🧠</div>
            <h3>AI Quiz Generator</h3>
            <p>Generate quizzes for different subjects and difficulty levels.
            Check your score and learn from explanations.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="info-card">
            <div class="big-icon">📅</div>
            <h3>Study Planner</h3>
            <p>Create a simple day-by-day plan for your chosen subject
            and make your study time more organized.</p>
        </div>
        <div class="info-card">
            <div class="big-icon">📈</div>
            <h3>Progress Tracker</h3>
            <p>Track the questions you ask, quizzes you finish,
            and your best quiz score during this session.</p>
        </div>
        """, unsafe_allow_html=True)

    st.info(
        "Tip: Choose a subject in the Study Assistant, or generate a quiz "
        "to test what you already know."
    )

# ---------- STUDY ASSISTANT ----------
elif page == "🤖 Study Assistant":
    st.markdown("""
    <div class="hero">
        <div class="small-label">YOUR PERSONAL TUTOR</div>
        <h1>AI Study Assistant 🤖</h1>
        <p>Ask a question and get a clear explanation tailored to your level.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("study_form"):
        col1, col2 = st.columns(2)

        with col1:
            topic = st.selectbox(
                "Choose a subject",
                [
                    "Python", "SQL", "Java", "Data Science",
                    "Machine Learning", "Pandas", "HTML and CSS",
                    "DBMS", "DSA", "Artificial Intelligence", "Other"
                ]
            )
            level = st.selectbox(
                "Your learning level",
                ["Beginner", "Intermediate", "Advanced"]
            )

        with col2:
            task = st.selectbox(
                "What type of help do you need?",
                [
                    "Explain", "Give examples", "Interview preparation",
                    "Give practice questions", "Give notes"
                ]
            )
            st.caption("Choose a topic and tell the mentor what you want to learn.")

        question = st.text_area(
            "Your question",
            placeholder="Example: Explain Python functions with a simple real-world example.",
            height=130
        )

        submitted = st.form_submit_button("✨ Generate my answer")

    if submitted:
        if not question.strip():
            st.warning("Please enter a question first.")
        elif not api_key:
            st.error("Add your Groq API key to the .env file.")
        else:
            with st.spinner("Your mentor is preparing an explanation..."):
                answer = explain_topic(
                    topic=topic,
                    question=question,
                    level=level,
                    task=task,
                    api_key=api_key
                )

            st.session_state.questions_asked += 1
            st.markdown("### Your study answer")
            st.markdown(answer)

            st.download_button(
                "⬇️ Download answer as a text file",
                data=(
                    f"Topic: {topic}\nLevel: {level}\nTask: {task}\n\n"
                    f"Question:\n{question}\n\nAnswer:\n{answer}"
                ),
                file_name="ai_study_notes.txt",
                mime="text/plain"
            )

# ---------- STUDY PLANNER ----------
elif page == "📅 Study Planner":
    st.markdown("""
    <div class="hero">
        <div class="small-label">BUILD A GOOD HABIT</div>
        <h1>Your Study Planner 📅</h1>
        <p>Turn a big learning goal into manageable daily tasks.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("planner_form"):
        subject = st.text_input(
            "What do you want to study?",
            placeholder="Example: Python for interviews"
        )

        col1, col2 = st.columns(2)
        with col1:
            days = st.slider("Plan duration (days)", 1, 30, 7)
        with col2:
            hours = st.slider("Study hours per day", 1, 8, 2)

        create_plan = st.form_submit_button("📌 Create my study plan")

    if create_plan:
        if not subject.strip():
            st.warning("Enter a subject to create your plan.")
        elif not api_key:
            st.error("Add your Groq API key to the .env file.")
        else:
            with st.spinner("Creating your study plan..."):
                plan = make_study_plan(subject, days, hours)

            st.markdown(plan)
            st.download_button(
                "⬇️ Download study plan",
                data=plan,
                file_name="my_study_plan.md",
                mime="text/markdown"
            )

    st.markdown("---")
    st.markdown("### A simple daily routine")
    r1, r2, r3 = st.columns(3)

    with r1:
        st.markdown("**📘 Learn**")
        st.caption("Understand one concept.")
    with r2:
        st.markdown("**💻 Practice**")
        st.caption("Write code or solve questions.")
    with r3:
        st.markdown("**🔁 Review**")
        st.caption("Summarize what you learned.")

# ---------- QUICK QUIZ ----------
elif page == "🧠 Quick Quiz":
    st.markdown("""
    <div class="hero">
        <div class="small-label">PRACTICE MAKES PROGRESS</div>
        <h1>AI Quiz Generator 🧠</h1>
        <p>Choose your subject, difficulty, and number of questions.
        Your AI mentor will create a new quiz for you.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### ⚙️ Customize your quiz")

        with st.form("quiz_setup_form"):
            col1, col2, col3 = st.columns(3)

            with col1:
                quiz_subject = st.selectbox(
                    "Choose a subject",
                    [
                        "Python",
                        "Java",
                        "SQL",
                        "Data Science",
                        "Machine Learning",
                        "Artificial Intelligence",
                        "HTML and CSS",
                        "DBMS",
                        "Data Structures and Algorithms",
                        "Pandas",
                        "Computer Networks",
                        "General Programming"
                    ],
                    key="quiz_subject_choice"
                )

            with col2:
                quiz_level = st.selectbox(
                    "Difficulty",
                    ["Beginner", "Intermediate", "Advanced"],
                    key="quiz_level_choice"
                )

            with col3:
                quiz_count = st.selectbox(
                    "Number of questions",
                    [5, 10, 15],
                    key="quiz_count_choice"
                )

            generate = st.form_submit_button(
                "✨ Generate my AI quiz",
                use_container_width=True
            )

        if generate:
            if not api_key:
                st.error("Groq API key not found. Please check your .env file.")
            else:
                try:
                    with st.spinner(
                        f"Creating {quiz_count} {quiz_subject} questions..."
                    ):
                        new_questions = generate_quiz(
                            subject=quiz_subject,
                            count=quiz_count,
                            level=quiz_level
                        )

                    st.session_state.quiz_questions = new_questions
                    st.session_state.quiz_result = None
                    st.session_state.quiz_subject = quiz_subject
                    st.session_state.quiz_level = quiz_level
                    st.session_state.quiz_count = quiz_count
                    st.success("Your new quiz is ready!")

                except Exception as e:
                    st.error(
                        "Unable to generate the quiz. Please try again."
                    )
                    st.caption(f"Technical details: {e}")

    questions = st.session_state.quiz_questions

    if questions:
        st.markdown("---")
        st.markdown(
            f"### 📝 {st.session_state.quiz_subject} Quiz"
        )
        st.caption(
            f"{len(questions)} questions · "
            f"{st.session_state.quiz_level} level"
        )

        with st.form("quiz_answers_form"):
            selected = {}

            for i, q in enumerate(questions):
                st.markdown(f"#### Question {i + 1}")
                st.markdown(q["q"])

                selected[i] = st.radio(
                    "Choose your answer",
                    q["options"],
                    index=None,
                    key=f"dynamic_quiz_{i}",
                    label_visibility="collapsed"
                )

                st.divider()

            submit_quiz = st.form_submit_button(
                "✅ Submit and check my score",
                use_container_width=True
            )

        if submit_quiz:
            score = sum(
                1 for i, q in enumerate(questions)
                if selected[i] == q["answer"]
            )

            percentage = round(score / len(questions) * 100)

            st.session_state.completed_quizzes += 1
            st.session_state.best_score = max(
                st.session_state.best_score,
                percentage
            )
            st.session_state.quiz_result = {
                "score": score,
                "percentage": percentage,
                "answers": selected.copy(),
                "questions": questions.copy()
            }

        result = st.session_state.quiz_result

        if result is not None:
            result_questions = result["questions"]
            score = result["score"]
            percentage = result["percentage"]

            st.markdown("---")
            st.markdown("## 🏆 Your quiz results")

            col1, col2, col3 = st.columns(3)
            col1.metric("Score", f"{score}/{len(result_questions)}")
            col2.metric("Percentage", f"{percentage}%")
            col3.metric(
                "Correct answers",
                f"{score} of {len(result_questions)}"
            )

            st.progress(
                percentage / 100,
                text=f"You scored {percentage}%"
            )

            if percentage == 100:
                st.success("Perfect score! Excellent work! 🎉")
            elif percentage >= 70:
                st.success("Great job! Review the explanations to improve further.")
            elif percentage >= 40:
                st.info("Good effort! Keep practicing and review your mistakes.")
            else:
                st.warning("Keep learning. Review the answers and try again.")

            st.markdown("### 📚 Answer review")

            for i, q in enumerate(result_questions):
                user_answer = result["answers"].get(i)
                correct_answer = q["answer"]

                st.markdown(f"**Question {i + 1}:** {q['q']}")

                if user_answer == correct_answer:
                    st.success(f"Your answer: {user_answer}")
                else:
                    st.error(
                        f"Your answer: {user_answer or 'Not answered'}"
                    )
                    st.markdown(f"**Correct answer:** {correct_answer}")

                st.info(f"**Explanation:** {q['why']}")
                st.markdown("---")

            report = [
                f"AI Study Mentor Quiz Results",
                f"Subject: {st.session_state.quiz_subject}",
                f"Difficulty: {st.session_state.quiz_level}",
                f"Score: {score}/{len(result_questions)} ({percentage}%)",
                ""
            ]

            for i, q in enumerate(result_questions):
                report.extend([
                    f"Question {i + 1}: {q['q']}",
                    f"Your answer: {result['answers'].get(i) or 'Not answered'}",
                    f"Correct answer: {q['answer']}",
                    f"Explanation: {q['why']}",
                    ""
                ])

            st.download_button(
                "⬇️ Download quiz results",
                data="\n".join(report),
                file_name="ai_quiz_results.txt",
                mime="text/plain"
            )

            if st.button("🔄 Generate another quiz", use_container_width=True):
                st.session_state.quiz_questions = []
                st.session_state.quiz_result = None
                st.rerun()

    else:
        st.info(
            "Choose your quiz settings above and click "
            "'Generate my AI quiz' to get started."
        )

# ---------- PROGRESS ----------
elif page == "📈 My Progress":
    st.markdown("""
    <div class="hero">
        <div class="small-label">YOUR LEARNING JOURNEY</div>
        <h1>My Progress 📈</h1>
        <p>See your activity in this session and keep building your skills.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Questions asked", st.session_state.questions_asked)
    col2.metric("Quizzes completed", st.session_state.completed_quizzes)
    col3.metric("Best score", f"{st.session_state.best_score}%")

    st.markdown("### Your current learning activity")

    if (
        st.session_state.questions_asked == 0
        and st.session_state.completed_quizzes == 0
    ):
        st.info(
            "Your activity will appear here after you ask a question "
            "or complete a quiz."
        )
    else:
        st.progress(
            st.session_state.best_score / 100,
            text="Best quiz score"
        )
        st.write(
            "Keep asking questions, practicing concepts, and revising your notes."
        )

    st.caption(
        "Progress is stored for the current app session and may reset "
        "when the session is restarted."
    )

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#93a2c5;font-size:12px;'>"
    "AI Study Mentor · Learn • Practice • Improve"
    "</div>",
    unsafe_allow_html=True
)
