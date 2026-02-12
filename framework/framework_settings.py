import os
from datetime import datetime

# Base project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Timestamp (if you need per-run subfolders later)
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# ---------- Reports root ----------
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# ---------- Allure ----------
ALLURE_RESULTS_DIR = os.path.join(REPORTS_DIR, "allure-results")
ALLURE_REPORT_DIR  = os.path.join(REPORTS_DIR, "allure-report")

# ---------- Artifacts ----------
VIDEOS_DIR       = os.path.join(REPORTS_DIR, "videos")
SCREENSHOTS_DIR  = os.path.join(REPORTS_DIR, "screenshots")
LOGS_DIR = os.path.join(REPORTS_DIR, "logs")

# --------- Shareable HTML summary ---------
SHAREABLE_REPORT_HTML = os.path.join(REPORTS_DIR, "shareable_report.html")

# Ensure directories exist
for path in [
    REPORTS_DIR,
    ALLURE_RESULTS_DIR,
    ALLURE_REPORT_DIR,
    VIDEOS_DIR,
    SCREENSHOTS_DIR,
    LOGS_DIR,
]:
    os.makedirs(path, exist_ok=True)

