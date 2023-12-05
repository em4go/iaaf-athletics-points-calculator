import streamlit as st

from lib import (
    calculate_performance,
    calculate_points,
    get_models,
    format_hours,
    format_mins,
    format_secs,
)

if "table_values" not in st.session_state:
    st.session_state["table_values"] = []

st.title("IAAF Scoring Calculator")

models = get_models()
meters_events = ["LJ", "TJ", "HJ", "SP", "DT", "HT", "JT", "PV"]
points_events = ["Decathlon", "Heptathlon"]

gender = st.selectbox("Choose gender", ("male", "female"), format_func=str.capitalize)

events = models[gender].keys()
event = st.selectbox("Select the event", (events))

tab1, tab2 = st.tabs(["Find points", "Find performance"])

with tab1:
    st.subheader("Lookup points based on performance")
    col1, col2, col3 = st.columns(3)
    if event in meters_events:
        seconds: float = st.number_input("meters", value=0.0, step=0.01, min_value=0.0)
        hours = 0
        minutes = 0
    elif event in points_events:
        hours = 0
        minutes = 0
        seconds: int = st.number_input("pts", value=0, step=1, min_value=0)
    else:
        hours: int = col1.number_input("hh", value=0, step=1, min_value=0)
        minutes: int = col2.number_input("mm", value=0, step=1, min_value=0)
        seconds: float = col3.number_input("ss:cc", value=0.0, step=0.01, min_value=0.0)
    hours_text = format_hours(hours)
    minutes_text = format_mins(minutes)
    seconds_text = format_secs(seconds)
    calculate_points_button = st.button("Calculate points")
    if calculate_points_button:
        performance = hours * 3600 + minutes * 60 + seconds
        if hours > 0:
            performance_text = f"{hours_text}:{minutes_text}:{seconds_text}"
        elif minutes > 0:
            performance_text = f"{minutes_text}:{seconds_text}"
        else:
            performance_text = f"{seconds_text}"
        coeffs = models[gender][event]
        points = calculate_points(coeffs, performance)
        st.session_state["table_values"].append(
            {
                "gender": gender,
                "event": event,
                "performance": performance_text,
                "points": points,
            }
        )

with tab2:
    st.subheader("Lookup performance based on points")
    points: int = st.number_input(
        "Points",
        value=0,
        step=1,
        min_value=0,
        max_value=1400,
    )
    calculate_performance_button = st.button(
        "Calculate performance",
    )
    if calculate_performance_button:
        coeffs = models[gender][event]
        performance = calculate_performance(coeffs, points)
        hours = performance // 3600
        minutes = (performance % 3600) // 60
        seconds = performance % 60

        seconds_text = format_secs(seconds)
        minutes_text = format_mins(minutes)
        hours_text = format_hours(hours)

        if hours > 0:
            performance_text = f"{hours_text}:{minutes_text}:{seconds_text}"
        elif minutes > 0:
            performance_text = f"{minutes_text}:{seconds_text}"
        else:
            performance_text = f"{seconds_text}"
        st.session_state["table_values"].append(
            {
                "gender": gender,
                "event": event,
                "performance": performance_text,
                "points": points,
            }
        )


col1, col2, col3, col4 = st.columns(4)


table = st.session_state["table_values"]
if len(table) > 0:
    "---"
    st.button("Clear table", on_click=lambda: st.session_state.pop("table_values"))
    st.table(table)
