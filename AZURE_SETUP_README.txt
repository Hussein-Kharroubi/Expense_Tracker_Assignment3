Azure App Service setup (EECE439 Assignment 7)

Upload the *contents* of this folder to the GitHub repository root, not the zip archive.
Azure: Linux App Service, Python 3.13 (or compatible supported Python runtime).
Deployment Center: GitHub; select Expense_Tracker_Assignment3 / main.
App Service > Settings > Environment variables > App settings:
  DJANGO_SECRET_KEY = a unique random secret string (keep private)
  SCM_DO_BUILD_DURING_DEPLOYMENT = true (if build is skipped)
App Service > Configuration > General settings > Startup Command: bash startup.sh
The startup script runs migrations and Gunicorn.
Check GitHub Actions deploy status, App Service Log stream, and test login/registration.

Note: the SQLite database stored at /home/site/data is acceptable only as a simple
classroom/demo workaround; App Service and SQLite locking/scaling can cause issues.
For reliable hosting use PostgreSQL instead. The original db.sqlite3 was not included
because it may contain personal data and should not be published on GitHub.
