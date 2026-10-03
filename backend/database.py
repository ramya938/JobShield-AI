import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


# ==========================================
# PostgreSQL Connection
# ==========================================

def get_connection():

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg2.connect(database_url)

    # Fallback for local PostgreSQL
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "jobshield_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD")
    )


# ==========================================
# Save Analysis
# ==========================================

def save_analysis(
    job_text,
    risk_score,
    risk_level,
    company_name,
    recommendation
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO analysis_history (
            job_text,
            risk_score,
            risk_level,
            company_name,
            recommendation
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            job_text,
            risk_score,
            risk_level,
            company_name,
            recommendation
        )
    )

    connection.commit()

    cursor.close()
    connection.close()


# ==========================================
# Get Analysis History
# ==========================================

def get_analysis_history():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            job_text,
            risk_score,
            risk_level,
            company_name,
            recommendation,
            created_at
        FROM analysis_history
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows