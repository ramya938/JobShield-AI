import psycopg2


# ==========================================
# PostgreSQL Connection
# ==========================================

def get_connection():

    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="jobshield_db",
        user="postgres",
        password="Ramya@1816"
    )

    return connection


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