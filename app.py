import random
import streamlit as st

# FIX: Refactored all game logic into logic_utils.py using Claude Code,
# so app.py only handles UI and app.py imports the fixed functions.
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

# Directional hint messages keyed by outcome
HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too Low": "📈 Go HIGHER!",
    "Too High": "📉 Go LOWER!",
}

# Temperature levels: (max_distance, label, hex_color)
TEMP_LEVELS = [
    (5,   "🔥 Scorching!",  "#FF4500"),
    (15,  "♨️  Hot",         "#FF8C00"),
    (25,  "😐 Warm",         "#FFA500"),
    (40,  "🌊 Cool",         "#4169E1"),
    (100, "❄️  Freezing!",   "#00BFFF"),
]


def get_temperature(guess: int, secret: int):
    """Return (label, color_hex) based on how close the guess is."""
    distance = abs(guess - secret)
    for threshold, label, color in TEMP_LEVELS:
        if distance <= threshold:
            return label, color
    return "❄️  Freezing!", "#00BFFF"


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(1, 100)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {Attempt, Guess, Direction, Temperature}

st.subheader("Make a guess")

st.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 1
    st.session_state.secret = random.randint(1, 100)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")

    # Summary table on game end
    if st.session_state.history:
        st.subheader("📋 Session Summary")
        st.dataframe(
            st.session_state.history,
            use_container_width=True,
            hide_index=True,
        )
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append({
            "Attempt": st.session_state.attempts - 1,
            "Guess": raw_guess,
            "Direction": "❌ Invalid",
            "Temperature": "—",
        })
        st.error(err)
    else:
        secret = st.session_state.secret
        outcome = check_guess(guess_int, secret)
        temp_label, temp_color = get_temperature(guess_int, secret)

        st.session_state.history.append({
            "Attempt": st.session_state.attempts - 1,
            "Guess": guess_int,
            "Direction": HINT_MESSAGES[outcome],
            "Temperature": "🎯 Bullseye" if outcome == "Win" else temp_label,
        })

        if show_hint and outcome != "Win":
            direction_msg = HINT_MESSAGES[outcome]
            st.markdown(
                f"<div style='padding:12px 16px; border-radius:8px; "
                f"background:{temp_color}22; border-left:5px solid {temp_color};'>"
                f"<span style='font-size:1.3em;'>{temp_label}</span>"
                f"&nbsp;&nbsp;<strong>{direction_msg}</strong>"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# Running guess history table (visible while game is in progress)
if st.session_state.history:
    st.subheader("📋 Guess History")
    st.dataframe(
        st.session_state.history,
        use_container_width=True,
        hide_index=True,
    )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
