import math
import json
import streamlit as st


@st.cache_data
def get_models():
    with open("iaaf_scoring_formulas.json") as f:
        models = json.load(f)
    return models


def calculate_performance(coeffs, points):
    a, b, c = coeffs  # ax**2 + bx + c = y
    # ax**2 + bx + c - y = 0
    # calculate -b +- sqrt(b^2 - 4a(c-y)) / 2a
    discriminant = b**2 - 4 * a * (c - points)
    if discriminant < 0:
        raise ValueError(
            "Points give a non-real performance. Are the constants correct?"
        )
    solutions = [
        (-b + math.sqrt(discriminant)) / (2 * a),
        (-b - math.sqrt(discriminant)) / (2 * a),
    ]
    return round(min(solution for solution in solutions if solution > 0), 2)


def calculate_points(coeffs, performance):
    a, b, c = coeffs  # ax**2 + bx + c = y
    points = round(a * performance**2 + b * performance + c)
    if points < 0:
        return 0
    if points > 1400:
        if calculate_performance(coeffs, 1400) < performance:
            return 0
        points = 1400
    return points
