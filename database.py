import sqlite3
from contextlib import closing
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().with_name("feedback.db")


def create_table():
    """Create the feedback table if it does not already exist."""
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS feedback (
                    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_name TEXT NOT NULL,
                    course_name TEXT NOT NULL,
                    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
                    comments TEXT
                )
                """
            )


def add_feedback(student_name, course_name, rating, comments):
    """Add one feedback record to the database."""
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        with connection:
            connection.execute(
                """
                INSERT INTO feedback (student_name, course_name, rating, comments)
                VALUES (?, ?, ?, ?)
                """,
                (student_name, course_name, rating, comments),
            )


def get_all_feedback():
    """Return all feedback records, oldest first."""
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        cursor = connection.execute(
            """
            SELECT feedback_id, student_name, course_name, rating, comments
            FROM feedback
            ORDER BY feedback_id
            """
        )
        return cursor.fetchall()


def get_average_rating():
    """Return the overall average rating, or None if there is no feedback."""
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        cursor = connection.execute("SELECT AVG(rating) FROM feedback")
        return cursor.fetchone()[0]


def get_highest_rated_course():
    """Return a list of courses tied for the highest average rating."""
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        cursor = connection.execute(
            """
            SELECT course_name, AVG(rating) AS average_rating
            FROM feedback
            GROUP BY course_name
            ORDER BY course_name
            """
        )
        course_ratings = cursor.fetchall()

    if not course_ratings:
        return []

    highest_average = max(average for _, average in course_ratings)
    return [
        course_name
        for course_name, average in course_ratings
        if average == highest_average
    ]


def get_course_summary():
    """Return (course_name, feedback_count, average_rating) for each course."""
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        cursor = connection.execute(
            """
            SELECT course_name, COUNT(*), ROUND(AVG(rating), 2)
            FROM feedback
            GROUP BY course_name
            ORDER BY course_name
            """
        )
        return cursor.fetchall()


if __name__ == "__main__":
    create_table()
    print(f"Database and feedback table are ready: {DATABASE_PATH}")
