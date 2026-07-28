from __future__ import annotations

import html
import json
import re
from datetime import datetime, timezone
from typing import Any

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from src.legal_engine import (
    ACTIVITIES,
    LegalLearningEngine,
    classify_learner_profile,
    get_quiz,
    load_topics,
    moderate_community_post,
    new_bandit_state,
    recommend_activity,
    update_bandit,
)

st.set_page_config(
    page_title="Teen Rights and Law Lab",
    page_icon="\u2696\ufe0f",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #15263d;
        --muted: #5c6b7a;
        --panel: #f5f8fc;
        --accent: #2f6fed;
        --accent-soft: #eaf1ff;
        --safe: #0b7a53;
        --warn: #a15c00;
    }
    .block-container {max-width: 1180px; padding-top: 1.6rem; padding-bottom: 3rem;}
    .hero {
        padding: 1.5rem 1.7rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #eef4ff 0%, #f8fbff 55%, #edf9f4 100%);
        border: 1px solid #d8e4f4;
        margin-bottom: 1rem;
    }
    .hero h1 {color: var(--ink); margin: 0 0 .45rem 0; font-size: 2.25rem;}
    .hero p {color: var(--muted); font-size: 1.05rem; margin: 0; max-width: 850px;}
    .soft-card {
        background: var(--panel);
        border: 1px solid #dfe7f0;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        min-height: 120px;
    }
    .response-card {
        border: 1px solid #d8e4f4;
        border-left: 5px solid var(--accent);
        background: #fbfdff;
        border-radius: 12px;
        padding: 1.1rem 1.2rem;
        margin-top: .8rem;
    }
    .safety-card {
        border: 1px solid #f1d19d;
        border-left: 5px solid #d67b00;
        background: #fff9ef;
        border-radius: 12px;
        padding: 1rem 1.1rem;
    }
    .credit-card {
        border: 1px solid #dfe7f0;
        border-radius: 12px;
        padding: .75rem .85rem;
        background: #f8fafc;
        margin-top: .8rem;
    }
    .small-muted {color: var(--muted); font-size: .9rem;}
    div[data-testid="stMetric"] {
        border: 1px solid #e0e7ef;
        border-radius: 12px;
        padding: .75rem;
        background: #fbfcfe;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_engine() -> LegalLearningEngine:
    return LegalLearningEngine()


@st.cache_data
def get_topics() -> dict[str, dict[str, Any]]:
    return load_topics()


def initialize_state() -> None:
    defaults: dict[str, Any] = {
        "question_history": [],
        "topic_counts": {},
        "topics_opened": [],
        "quiz_attempts": 0,
        "quiz_correct": 0,
        "quiz_cursor": {},
        "quiz_answered_key": "",
        "quiz_feedback": None,
        "community_posts": [
            {
                "title": "How do I check whether a school rule is written down?",
                "body": "Start with the student handbook, then ask a counselor or administrator which policy applies.",
                "topic": "School Rights",
            },
            {
                "title": "What should a teen save after an online purchase?",
                "body": "The receipt, product description, seller messages, and cancellation or refund terms are useful.",
                "topic": "Contracts and Money",
            },
        ],
        "community_posts_created": 0,
        "last_answer": None,
        "bandit": new_bandit_state(),
        "recommended_activity": "Ask the Rights Guide",
        "recommendation_feedback": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def record_topic(topic_id: str) -> None:
    if topic_id in {"safety_support", "safe_alternatives"}:
        return
    counts = st.session_state.topic_counts
    counts[topic_id] = counts.get(topic_id, 0) + 1
    if topic_id not in st.session_state.topics_opened:
        st.session_state.topics_opened.append(topic_id)


def log_question(result: dict[str, Any]) -> None:
    st.session_state.question_history.append(
        {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "topic": result["topic_label"],
            "safety_level": result["safety_level"],
            "routing_score": round(float(result["routing_score"]), 3),
        }
    )
    record_topic(result["topic_id"])


def plain_for_speech(result: dict[str, Any]) -> str:
    parts = [
        result["topic_label"],
        result["plain_language"],
        "Key ideas.",
        *result["key_points"],
        "Possible next steps.",
        *result["next_steps"],
        result["jurisdiction_note"],
        result["disclaimer"],
    ]
    text = " ".join(parts)
    return re.sub(r"\s+", " ", text).strip()


def render_speech_component(text: str) -> None:
    script_text = json.dumps(text)
    components.html(
        f"""
        <script>
        const message = new SpeechSynthesisUtterance({script_text});
        message.rate = 0.95;
        message.pitch = 1.0;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(message);
        </script>
        """,
        height=1,
    )


def render_footer() -> None:
    st.divider()
    st.caption(
        "Teen Rights and Law Lab is an educational prototype. It is not legal advice and should not be used during an emergency."
    )


def render_home(topics: dict[str, dict[str, Any]]) -> None:
    st.markdown(
        """
        <div class="hero">
          <h1>Teen Rights and Law Lab</h1>
          <p>Learn legal ideas in everyday language, practice with mini-games, and explore safe next steps without sharing private information.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.warning(
        "This prototype provides general education only. Laws vary by location and facts. Use a qualified local lawyer or legal-aid organization for advice about a real case."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="soft-card"><h3>Ask in plain language</h3><p>Type a question and the transparent NLP router finds the closest reviewed topic.</p></div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="soft-card"><h3>Practice safely</h3><p>Mini-games focus on evidence, privacy, trusted support, and lawful next steps.</p></div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class="soft-card"><h3>Protect privacy</h3><p>The demo has no login and keeps progress only in the current browser session.</p></div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Explore a topic")
    topic_ids = list(topics.keys())
    for row_start in range(0, min(len(topic_ids), 9), 3):
        columns = st.columns(3)
        for offset, topic_id in enumerate(topic_ids[row_start : row_start + 3]):
            topic = topics[topic_id]
            with columns[offset]:
                st.markdown(f"**{topic['short_label']}**")
                st.write(topic["summary"])
                st.caption(f"Try: {topic['example_questions'][0]}")

    st.info(
        "Safety rule: reinforcement learning in this prototype may recommend a learning activity, but it is never allowed to rewrite legal content, safety messages, or moderation rules."
    )
    render_footer()


def render_ask(engine: LegalLearningEngine) -> None:
    st.title("Ask the Rights Guide")
    st.write(
        "Ask a general question. Do not enter names, contact details, school identifiers, account credentials, or a home address."
    )

    with st.form("ask_form"):
        question = st.text_area(
            "Your question",
            height=130,
            placeholder="Example: What should I save if someone is threatening me online?",
        )
        col1, col2 = st.columns(2)
        with col1:
            jurisdiction = st.text_input(
                "Country or state (optional)",
                placeholder="Example: Maryland",
                help="This is not verified. Never enter a street address.",
            )
        with col2:
            reading_style = st.selectbox(
                "Explanation style",
                ["Quick and clear", "Step by step", "Key ideas first"],
            )
        submitted = st.form_submit_button("Explain this topic", type="primary", use_container_width=True)

    if submitted:
        if len(question.strip()) < 5:
            st.error("Please enter a complete question without private information.")
        else:
            result = engine.answer(question, jurisdiction).to_dict()
            result["reading_style"] = reading_style
            st.session_state.last_answer = result
            log_question(result)

    result = st.session_state.last_answer
    if result:
        card_class = "safety-card" if result["safety_level"] in {"critical", "high", "blocked"} else "response-card"
        safe_heading = html.escape(result["topic_label"])
        safe_body = html.escape(result["plain_language"])
        st.markdown(
            f'<div class="{card_class}"><h3>{safe_heading}</h3><p>{safe_body}</p></div>',
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Key ideas")
            for item in result["key_points"]:
                st.markdown(f"- {item}")
        with c2:
            st.markdown("### Possible next steps")
            for item in result["next_steps"]:
                st.markdown(f"- {item}")

        st.info(result["jurisdiction_note"])
        st.caption(result["disclaimer"])
        st.caption(
            f"Topic-routing match: {result['routing_score']:.0%}. This measures text similarity, not legal certainty."
        )

        read_col, clear_col = st.columns(2)
        with read_col:
            if st.button("Read this answer aloud", use_container_width=True):
                render_speech_component(plain_for_speech(result))
        with clear_col:
            if st.button("Clear answer", use_container_width=True):
                st.session_state.last_answer = None
                st.rerun()

    render_footer()


def render_learn(topics: dict[str, dict[str, Any]]) -> None:
    st.title("Learn the Law in Everyday Language")
    label_to_id = {topic["label"]: topic_id for topic_id, topic in topics.items()}
    selected_label = st.selectbox("Choose a topic", list(label_to_id.keys()))
    topic_id = label_to_id[selected_label]
    topic = topics[topic_id]
    record_topic(topic_id)

    st.markdown(f"## {topic['label']}")
    st.write(topic["summary"])

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### What to understand")
        for item in topic["key_points"]:
            st.markdown(f"- {item}")
    with col2:
        st.markdown("### A safer action plan")
        for item in topic["next_steps"]:
            st.markdown(f"- {item}")

    st.info(f"Common myth: {topic['myth']}")
    st.markdown("### Questions to explore")
    for question in topic["example_questions"]:
        st.markdown(f"- {question}")

    st.caption(
        "The topic library is intentionally general. A qualified reviewer should validate every jurisdiction-specific addition before release."
    )
    render_footer()


def render_quiz(topics: dict[str, dict[str, Any]]) -> None:
    st.title("Mini-Games and Knowledge Checks")
    quiz_topics = {topic["short_label"]: topic_id for topic_id, topic in topics.items() if topic.get("quiz")}
    selected_label = st.selectbox("Choose a mini-game topic", list(quiz_topics.keys()))
    topic_id = quiz_topics[selected_label]
    questions = get_quiz(topic_id)
    cursor = st.session_state.quiz_cursor.get(topic_id, 0) % len(questions)
    question = questions[cursor]
    question_key = f"{topic_id}:{cursor}"

    st.markdown(f"### Question {cursor + 1} of {len(questions)}")
    st.write(question["question"])
    selected = st.radio(
        "Choose one answer",
        range(len(question["options"])),
        format_func=lambda index: question["options"][index],
        key=f"choice_{question_key}",
    )

    answered = st.session_state.quiz_answered_key == question_key
    if st.button("Check answer", type="primary", disabled=answered):
        correct = selected == question["answer"]
        st.session_state.quiz_attempts += 1
        st.session_state.quiz_correct += int(correct)
        st.session_state.quiz_answered_key = question_key
        st.session_state.quiz_feedback = {
            "correct": correct,
            "explanation": question["explanation"],
            "correct_option": question["options"][question["answer"]],
        }
        record_topic(topic_id)
        st.rerun()

    if answered and st.session_state.quiz_feedback:
        feedback = st.session_state.quiz_feedback
        if feedback["correct"]:
            st.success("Correct. " + feedback["explanation"])
        else:
            st.error("Not quite. The best answer is: " + feedback["correct_option"])
            st.info(feedback["explanation"])
        if st.button("Next question", use_container_width=True):
            st.session_state.quiz_cursor[topic_id] = cursor + 1
            st.session_state.quiz_answered_key = ""
            st.session_state.quiz_feedback = None
            st.rerun()

    attempts = st.session_state.quiz_attempts
    accuracy = (st.session_state.quiz_correct / attempts) if attempts else 0.0
    c1, c2 = st.columns(2)
    c1.metric("Questions completed", attempts)
    c2.metric("Accuracy", f"{accuracy:.0%}")
    render_footer()


def render_community(topics: dict[str, dict[str, Any]]) -> None:
    st.title("Moderated Community Lab")
    st.write(
        "This is a session-only prototype. It demonstrates pre-post moderation and does not publish content to the internet or save it after the session ends."
    )
    st.warning("Never post names, phone numbers, email addresses, street addresses, account details, or sensitive images.")

    topic_labels = [topic["short_label"] for topic in topics.values()]
    with st.form("community_form", clear_on_submit=True):
        title = st.text_input("Discussion title", max_chars=120)
        topic = st.selectbox("Topic", topic_labels)
        body = st.text_area("Post", max_chars=1200, height=120)
        post_submitted = st.form_submit_button("Run safety check and post", type="primary")

    if post_submitted:
        result = moderate_community_post(title, body)
        if result.allowed:
            st.session_state.community_posts.insert(
                0,
                {"title": title.strip(), "body": body.strip(), "topic": topic},
            )
            st.session_state.community_posts_created += 1
            st.success("The post passed the prototype safety check and was added to this session.")
        else:
            st.error("This post was not added.")
            for reason in result.reasons:
                st.markdown(f"- {reason}")
            if result.support_message:
                st.warning(result.support_message)

    st.subheader("Session discussions")
    for index, post in enumerate(st.session_state.community_posts):
        with st.container(border=True):
            st.caption(post["topic"] + " | Anonymous participant")
            st.markdown(f"### {html.escape(post['title'])}")
            st.write(post["body"])
            st.caption("Prototype reminder: verify legal claims before relying on them.")

    render_footer()


def render_progress(topics: dict[str, dict[str, Any]]) -> None:
    st.title("Learning Progress and AI Methods")
    attempts = st.session_state.quiz_attempts
    accuracy = (st.session_state.quiz_correct / attempts) if attempts else 0.0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Questions asked", len(st.session_state.question_history))
    c2.metric("Topics explored", len(st.session_state.topics_opened))
    c3.metric("Quiz accuracy", f"{accuracy:.0%}")
    c4.metric("Community posts", st.session_state.community_posts_created)

    if st.session_state.topic_counts:
        st.subheader("Topic activity")
        chart_rows = [
            {
                "Topic": topics[topic_id]["short_label"],
                "Interactions": count,
            }
            for topic_id, count in st.session_state.topic_counts.items()
            if topic_id in topics
        ]
        chart_df = pd.DataFrame(chart_rows).set_index("Topic")
        st.bar_chart(chart_df)

    st.subheader("K-means learner profile demonstration")
    st.caption(
        "This demo clusters learning preferences only. It does not use identity, race, religion, health, precise location, or other sensitive demographic data."
    )
    col1, col2 = st.columns(2)
    with col1:
        quiz_confidence = st.slider("Quiz confidence", 0, 100, 60)
        exploration = st.slider("Interest in exploring new topics", 0, 100, 70)
    with col2:
        discussion_interest = st.slider("Interest in moderated discussion", 0, 100, 55)
        safety_awareness = st.slider("Safety and privacy awareness", 0, 100, 80)

    profile = classify_learner_profile(
        quiz_confidence, exploration, discussion_interest, safety_awareness
    )
    st.success(f"Learning style: {profile['label']}")
    st.write(profile["suggestion"])
    with st.expander("See the demonstration cluster center"):
        st.json(profile["center"])

    st.subheader("Bounded reinforcement-learning recommendation")
    st.caption(
        "The epsilon-greedy bandit learns only which learning activity feels useful. It cannot change legal explanations, emergency messages, or moderation rules."
    )
    if st.button("Recommend my next activity", type="primary"):
        st.session_state.recommended_activity = recommend_activity(st.session_state.bandit)
        st.session_state.recommendation_feedback = ""

    activity = st.session_state.recommended_activity
    st.info(f"Recommended next activity: {activity}")
    good_col, bad_col = st.columns(2)
    with good_col:
        if st.button("Helpful recommendation", use_container_width=True):
            update_bandit(st.session_state.bandit, activity, 1.0)
            st.session_state.recommendation_feedback = "Thanks. The activity score was updated."
    with bad_col:
        if st.button("Not helpful yet", use_container_width=True):
            update_bandit(st.session_state.bandit, activity, 0.0)
            st.session_state.recommendation_feedback = "Thanks. The activity score was updated."
    if st.session_state.recommendation_feedback:
        st.caption(st.session_state.recommendation_feedback)

    with st.expander("See activity values"):
        values_df = pd.DataFrame(
            {
                "Activity": ACTIVITIES,
                "Estimated helpfulness": [st.session_state.bandit["values"][name] for name in ACTIVITIES],
                "Feedback count": [int(st.session_state.bandit["counts"][name]) for name in ACTIVITIES],
            }
        )
        st.dataframe(values_df, use_container_width=True, hide_index=True)

    export = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "questions_asked": len(st.session_state.question_history),
        "topics_explored": [topics[topic_id]["short_label"] for topic_id in st.session_state.topics_opened],
        "quiz_attempts": st.session_state.quiz_attempts,
        "quiz_correct": st.session_state.quiz_correct,
        "community_posts_created": st.session_state.community_posts_created,
        "question_history_without_question_text": st.session_state.question_history,
        "activity_values": st.session_state.bandit,
    }
    st.download_button(
        "Download my session progress (JSON)",
        data=json.dumps(export, indent=2),
        file_name="teen_law_learning_progress.json",
        mime="application/json",
        use_container_width=True,
    )
    render_footer()


def render_about() -> None:
    st.title("About, Safety, and Development Roadmap")
    st.markdown("### Project credits")
    st.write("**Author:** Arya Patel")
    st.write("**Mentor:** Dr. Qingyang Xiao")

    st.markdown("### What works in this prototype")
    st.markdown(
        """
        - Transparent TF-IDF natural-language topic routing.
        - A reviewed local legal-education knowledge base.
        - Rule-based safety screening before every response.
        - Mini-games with session-only progress tracking.
        - K-means clustering of non-sensitive learning preferences.
        - A bounded epsilon-greedy activity recommender.
        - Community-post moderation for obvious privacy and safety risks.
        - Browser text-to-speech for generated educational responses.
        """
    )

    st.markdown("### What is intentionally not claimed")
    st.markdown(
        """
        - The prototype is not a lawyer, court, emergency service, or verified legal database.
        - It does not provide a legal conclusion for a real case.
        - It does not use a production LLM or deep neural network yet.
        - It does not retain accounts, demographic profiles, private messages, or community data.
        - It does not allow reinforcement learning to self-modify legal or safety rules.
        """
    )

    st.markdown("### Responsible path toward a production app")
    st.markdown(
        """
        1. Have qualified legal reviewers validate each jurisdiction-specific content module.
        2. Add youth-safety, privacy, accessibility, and moderation testing before collecting user data.
        3. Use retrieval from versioned, cited legal sources rather than unconstrained model memory.
        4. Add human escalation, incident logging, appeals, and content-review workflows.
        5. Build an authenticated Python API for a separate SwiftUI iOS client.
        6. Complete security, app-store, open-source license, and intellectual-property reviews before release.
        """
    )

    st.info(
        "The repository includes an iOS roadmap, deployment guide, content-review checklist, open-source license, and a Colab notebook."
    )
    render_footer()


initialize_state()
engine = get_engine()
topics = get_topics()

st.sidebar.markdown("## Teen Rights and Law Lab")
st.sidebar.caption("Law education in everyday language")
page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Ask the Rights Guide",
        "Learn",
        "Mini-Games",
        "Community Lab",
        "Progress and AI",
        "About and Safety",
    ],
)
st.sidebar.markdown(
    """
    <div class="credit-card">
      <strong>Project credits</strong><br>
      Author: Arya Patel<br>
      Mentor: Dr. Qingyang Xiao
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.caption("Educational only - not legal advice")

if page == "Home":
    render_home(topics)
elif page == "Ask the Rights Guide":
    render_ask(engine)
elif page == "Learn":
    render_learn(topics)
elif page == "Mini-Games":
    render_quiz(topics)
elif page == "Community Lab":
    render_community(topics)
elif page == "Progress and AI":
    render_progress(topics)
else:
    render_about()
