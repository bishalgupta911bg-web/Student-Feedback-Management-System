import streamlit as st
import altair as alt

from database import (
    add_feedback,
    create_table,
    get_all_feedback,
    get_average_rating,
    get_course_summary,
    get_highest_rated_course,
)


COURSES = [
    "Python",
    "Java",
    "C Programming",
    "Data Structures",
    "Database Management Systems",
]
NAVIGATION = ["DASHBOARD", "SUBMIT FEEDBACK", "VIEW FEEDBACK", "ANALYTICS"]

def submit_feedback():
    student_name = st.session_state.get("student_name", "").strip()
    course_name = st.session_state.get("course_name")
    rating = st.session_state.get("rating", 5)
    comments = st.session_state.get("comments", "").strip()

    if not student_name:
        st.session_state["form_error"] = "Enter your name before submitting feedback."
    elif course_name is None:
        st.session_state["form_error"] = "Choose a course before submitting feedback."
    else:
        add_feedback(student_name, course_name, int(rating), comments or None)
        st.session_state["success_message"] = "Your feedback was submitted successfully."
        st.session_state["navigation"] = "DASHBOARD"
        st.session_state.pop("form_error", None)

st.set_page_config(
    page_title="Student Feedback | Campus",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --green: #23734f;
        --green-dark: #174b35;
        --green-soft: #e8f2ec;
        --ink: #20352a;
        --muted: #64746a;
        --line: #dce5df;
    }

    .stApp {
        background: linear-gradient(145deg, #f8fbf9 0%, #eef3f0 100%);
        color: var(--ink);
    }

    [data-testid="stHeader"],
    [data-testid="stToolbar"] {
        background: #f8fbf9 !important;
        color: var(--green-dark) !important;
    }

    [data-testid="stHeader"] button,
    [data-testid="stHeader"] button svg {
        color: var(--green-dark) !important;
        fill: currentColor;
    }

    [data-testid="stSidebar"] {
        background: #e8f2ec;
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] label *,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"],
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] * {
        color: var(--green-dark) !important;
        opacity: 1 !important;
    }

    .block-container {
        max-width: 1280px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: var(--green-dark);
    }

    [data-testid="stMetric"] {
        height: 100%;
        min-height: 132px;
        padding: 1.1rem 1.25rem;
        border: 1px solid var(--line);
        border-left: 4px solid var(--green);
        border-radius: 8px;
        background: #ffffff;
        box-shadow: 0 2px 8px rgba(27, 67, 46, 0.05);
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] *,
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        color: var(--green-dark) !important;
        white-space: normal !important;
        overflow: visible !important;
        overflow-wrap: break-word;
        word-break: normal !important;
        opacity: 1 !important;
    }

    [data-testid="stMetricValue"] * {
        font-size: 1.5rem !important;
        line-height: 1.25;
    }

    button[kind="primary"] {
        background: var(--green);
        border-color: var(--green);
    }

    button[kind="primary"]:hover {
        background: var(--green-dark);
        border-color: var(--green-dark);
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1.25rem 1rem 2rem;
        }
    }

    @media (max-width: 640px) {
        [data-testid="stHorizontalBlock"] {
            flex-direction: column;
            gap: 0.75rem;
        }

        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100%;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

create_table()

with st.sidebar:
    st.markdown("## CAMPUS / VOICE")
    st.caption("STUDENT FEEDBACK")
    selected_page = st.radio(
        "NAVIGATION",
        NAVIGATION,
        key="navigation",
        label_visibility="visible",
    )
    st.markdown("---")
    st.caption("Academic feedback dashboard")

feedback_records = get_all_feedback()
overall_average = get_average_rating()
highest_rated_courses = get_highest_rated_course()
course_summary = get_course_summary()

st.caption("ACADEMIC SERVICES  /  STUDENT VOICE")
st.title(selected_page.title())

if "success_message" in st.session_state:
    st.success(st.session_state.pop("success_message"))

if selected_page == "DASHBOARD":
    first_metric_row = st.columns(2, gap="large")
    second_metric_row = st.columns(2, gap="large")
    highest_label = ", ".join(highest_rated_courses) if highest_rated_courses else "N/A"
    average_label = f"{overall_average:.2f} / 5" if overall_average is not None else "N/A"

    with first_metric_row[0]:
        st.metric("Total submissions", len(feedback_records), border=True)
    with first_metric_row[1]:
        st.metric("Overall average", average_label, border=True)
    with second_metric_row[0]:
        st.metric("Highest-rated course", highest_label, border=True)
    with second_metric_row[1]:
        st.metric("Total courses", len(COURSES), border=True)

    st.markdown("### Recent feedback")
    if feedback_records:
        recent_records = feedback_records[-5:][::-1]
        st.dataframe(
            [
                {
                    "ID": record[0],
                    "Student": record[1],
                    "Course": record[2],
                    "Rating": record[3],
                    "Comments": record[4] or "",
                }
                for record in recent_records
            ],
            hide_index=True,
            width="stretch",
        )
    else:
        st.info("No feedback has been submitted yet.")

elif selected_page == "SUBMIT FEEDBACK":
    st.markdown("### Share your course feedback")

    with st.form("feedback_form", clear_on_submit=True):
        name_column, course_column = st.columns(2)
        with name_column:
            st.text_input("Student Name", max_chars=100, key="student_name")
        with course_column:
            course_name = st.selectbox(
                "Course Name",
                COURSES,
                index=None,
                placeholder="Choose a course",
                key="course_name",
            )

        st.selectbox(
            "Rating",
            options=[1, 2, 3, 4, 5],
            index=4,
            format_func=lambda value: f"{value} / 5",
            key="rating",
        )
        st.text_area("Comments", max_chars=1000, height=140, key="comments")
        st.form_submit_button(
            "Submit feedback",
            type="primary",
            width="stretch",
            on_click=submit_feedback,
        )

    if "form_error" in st.session_state:
        st.error(st.session_state["form_error"])

elif selected_page == "VIEW FEEDBACK":
    if not feedback_records:
        st.info("No feedback records to display yet.")
    else:
        course_options = ["All courses"] + [row[0] for row in course_summary]
        selected_course = st.selectbox("Filter by course", course_options)
        visible_records = [
            record
            for record in feedback_records
            if selected_course == "All courses" or record[2] == selected_course
        ]
        st.caption(f"Showing {len(visible_records)} of {len(feedback_records)} submissions")
        st.dataframe(
            [
                {
                    "feedback_id": record[0],
                    "student_name": record[1],
                    "course_name": record[2],
                    "rating": record[3],
                    "comments": record[4] or "",
                }
                for record in visible_records
            ],
            hide_index=True,
            width="stretch",
        )

elif selected_page == "ANALYTICS":
    analytics_columns = st.columns(3, gap="large")
    average_label = f"{overall_average:.2f} / 5" if overall_average is not None else "N/A"
    highest_label = ", ".join(highest_rated_courses) if highest_rated_courses else "No ratings yet"

    with analytics_columns[0]:
        st.metric("Overall average rating", average_label, border=True)
    with analytics_columns[1]:
        st.metric("Highest-rated course(s)", highest_label, border=True)
    with analytics_columns[2]:
        st.metric("Total feedback submissions", len(feedback_records), border=True)

    if course_summary:
        st.markdown("### Course-wise rating summary")
        st.dataframe(
            [
                {
                    "Course": course,
                    "Total feedback": count,
                    "Average rating": average,
                }
                for course, count, average in course_summary
            ],
            hide_index=True,
            width="stretch",
        )

        st.markdown("### Average rating by course")
        chart_data = [
            {"Course": course, "Average rating": average}
            for course, _, average in course_summary
        ]
        rating_chart = (
            alt.Chart(alt.Data(values=chart_data))
            .mark_bar(color="#23734f", cornerRadiusEnd=3)
            .encode(
                x=alt.X(
                    "Average rating:Q",
                    scale=alt.Scale(domain=[0, 5]),
                    axis=alt.Axis(
                        title="Average rating (out of 5)",
                        values=[0, 1, 2, 3, 4, 5],
                    ),
                ),
                y=alt.Y(
                    "Course:N",
                    sort=alt.SortField(field="Average rating", order="descending"),
                    axis=alt.Axis(
                        title="Course",
                        labelLimit=0,
                        labelOverlap=False,
                    ),
                ),
                tooltip=[
                    alt.Tooltip("Course:N"),
                    alt.Tooltip("Average rating:Q", format=".2f"),
                ],
            )
            .properties(height=max(300, len(chart_data) * 58))
        )
        st.altair_chart(rating_chart, width="stretch")
    else:
        st.info("Course analytics will appear after feedback is submitted.")
