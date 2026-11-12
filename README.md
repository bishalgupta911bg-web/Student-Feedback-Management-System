# Student Feedback Management System

A Streamlit application for submitting and reviewing course feedback. It stores records in a local SQLite database and provides dashboard metrics and course rating analytics.

## Project Objective

Provide a simple web application where students can submit course ratings and comments, while administrators can review submissions and analyze overall and course-wise ratings.

## Technologies Used

- **Python** - application logic and database access.
- **Streamlit** - web interface and dashboard.
- **SQLite** - local storage for feedback records.
- **Git** - source control and project history.

## Features

- Submit a student's name, course, 1–5 rating, and optional comments.
- View and filter feedback records by course.
- See the total number of submissions, overall average rating, highest-rated course, and course-wise totals and averages.
- Compare average course ratings in a bar chart. Tied highest-rated courses are all shown.

## Database Structure

The application uses `feedback.db`, a SQLite database located beside `database.py`. The `feedback` table contains one row per submitted response:

| Column | Type | Description |
| --- | --- | --- |
| `feedback_id` | INTEGER | Auto-incrementing primary key for a feedback record. |
| `student_name` | TEXT | Student's name; required. |
| `course_name` | TEXT | Course name; required. |
| `rating` | INTEGER | Required rating from 1 through 5, enforced by a database constraint. |
| `comments` | TEXT | Optional written comments. |

The app creates the table at startup if it does not already exist. Existing feedback remains in the database between runs.

## Project Folder Structure

```text
Assestment/
├── .venv/              # Local Python virtual environment
├── __pycache__/        # Generated Python bytecode cache
├── app.py              # Streamlit application and dashboard
├── database.py         # SQLite setup and feedback functions
├── feedback.db         # Local database and feedback records
├── README.md           # Project documentation
└── requirements.txt    # Python package dependencies
```

The `.venv/` and `__pycache__/` folders are generated locally and do not need to be submitted to GitHub.

## Requirements

- Python 3.10 or later
- Git

SQLite is included with Python. The packages required by the app are listed in `requirements.txt`.

## Install Dependencies on Windows PowerShell

Open PowerShell in the project folder and create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project's dependencies from `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

If PowerShell activation is unavailable, install dependencies using the virtual environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Then run the app using that Python directly:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Run the Application

With the virtual environment activated and dependencies installed, start the app from the project folder:

```powershell
streamlit run app.py
```

Streamlit prints a local URL, usually `http://localhost:8501`, to open in a browser. Stop the server with `Ctrl+C` in the terminal.

## Testing

The following is a manual test checklist, not a report of completed test results:

1. **Feedback submission:** Submit a valid name, course, rating, and optional comments. Check that the app confirms the submission. Also try leaving the name blank and confirm validation prevents submission.
2. **Feedback retrieval:** Open **View Feedback** and confirm the submitted record appears with its ID, student, course, rating, and comments. Try filtering by course.
3. **Average rating:** Use known ratings and compare the displayed overall average with their sum divided by their count. Confirm the empty-data state is clear before any feedback exists.
4. **Highest-rated course:** Submit ratings for at least two courses, compare their averages, and check that the course with the highest average is shown. If courses tie, confirm all tied courses are shown.
5. **Course-wise summary:** For each course, compare the displayed feedback total and average against its submitted records.

## Git and GitHub

Git records changes to project files so they can be reviewed and restored. To start tracking the source files and make a commit:

```powershell
git init
git add app.py database.py README.md requirements.txt
git commit -m "Add student feedback management system"
```

To submit the project to a GitHub repository, create an empty repository on GitHub, then connect and push it:

```powershell
git branch -M main
git remote add origin https://github.com/<username>/<repository>.git
git push -u origin main
```

Replace `<username>` and `<repository>` with the GitHub account and repository name. Review staged files before committing, and do not publish `feedback.db` if it contains real student information.

