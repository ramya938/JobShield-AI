import { useState } from "react";
import "./App.css";

// Backend base URL (set VITE_API_BASE_URL when deploying; defaults to local Docker)
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8001";

function App() {
  const [jobText, setJobText] = useState("");
  const [jobUrl, setJobUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Analysis history
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);

  // ==========================================
  // Analyze Job Description
  // ==========================================
  const analyzeText = async () => {
    if (!jobText.trim()) {
      alert("Please enter a job description.");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          job_text: jobText,
        }),
      });

      if (!response.ok) {
        throw new Error("Backend error");
      }

      const data = await response.json();
      setResult(data.analysis);

      if (showHistory) {
        await loadHistory();
      }
    } catch (error) {
      console.error(error);
      alert("Could not connect to JobShield AI backend.");
    } finally {
      setLoading(false);
    }
  };

  // ==========================================
  // Analyze Job URL
  // ==========================================
  const analyzeUrl = async () => {
    if (!jobUrl.trim()) {
      alert("Please enter a job URL.");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/analyze-url`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: jobUrl,
        }),
      });

      if (!response.ok) {
        throw new Error("Backend error");
      }

      const data = await response.json();

      if (!data.success) {
        alert(data.error || "Could not analyze URL.");
        return;
      }

      setResult(data.analysis);

      if (showHistory) {
        await loadHistory();
      }
    } catch (error) {
      console.error(error);
      alert("Could not connect to JobShield AI backend.");
    } finally {
      setLoading(false);
    }
  };

  // ==========================================
  // Load Analysis History
  // ==========================================
  const loadHistory = async () => {
    setHistoryLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/history`);

      if (!response.ok) {
        throw new Error("Could not load history");
      }

      const data = await response.json();
      setHistory(data.history || []);
      setShowHistory(true);
    } catch (error) {
      console.error(error);
      alert("Could not load analysis history.");
    } finally {
      setHistoryLoading(false);
    }
  };

  // ==========================================
  // Risk Class
  // ==========================================
  const getRiskClass = (score, riskLevel) => {
    if (riskLevel === "NOT A JOB POSTING") {
      return "not-job";
    }

    if (score >= 61) {
      return "high-risk";
    }

    if (score >= 31) {
      return "medium-risk";
    }

    return "low-risk";
  };

  // ==========================================
  // Risk Icon
  // ==========================================
  const getRiskIcon = (score, riskLevel) => {
    if (riskLevel === "NOT A JOB POSTING") {
      return "⚪";
    }

    if (score >= 61) {
      return "🔴";
    }

    if (score >= 31) {
      return "🟡";
    }

    return "🟢";
  };

  // ==========================================
  // Company Verification Class
  // ==========================================
  const getCompanyStatusClass = (status) => {
    if (!status) {
      return "status-unknown";
    }

    const value = status.toLowerCase();

    if (value === "strong") {
      return "status-strong";
    }

    if (value === "weak" || value === "needs verification") {
      return "status-warning";
    }

    return "status-unknown";
  };

  // ==========================================
  // Main UI
  // ==========================================
  return (
    <div className="app">
      {/* ======================================
          HEADER
          ====================================== */}
      <header className="hero-header">
        <div className="brand">
          <span className="shield">🛡️</span>
          <h1>JobShield AI</h1>
        </div>

        <p>AI-powered Fake Job & Internship Detection System</p>

        <span className="status-badge">● AI Protection Active</span>
      </header>

      {/* ======================================
          MAIN
          ====================================== */}
      <main>
        {/* ====================================
            INPUT CARD
            ==================================== */}
        <section className="input-card">
          <div className="section-title">
            <span className="title-icon">🔍</span>
            <div>
              <h2>Check a Job or Internship</h2>
              <p>Analyze suspicious job postings before you apply.</p>
            </div>
          </div>

          {/* Job Description */}
          <label>Job / Internship Description</label>

          <textarea
            placeholder="Paste the complete job or internship description here..."
            value={jobText}
            onChange={(e) => setJobText(e.target.value)}
          />

          {/* Analyze Job */}
          <button
            type="button"
            className="primary-button"
            onClick={analyzeText}
            disabled={loading}
          >
            {loading ? "🔄 Analyzing..." : "🛡️ Analyze Job"}
          </button>

          {/* Divider */}
          <div className="divider">
            <span></span>
            <strong>OR</strong>
            <span></span>
          </div>

          {/* URL */}
          <label>Job Posting URL</label>

          <input
            type="text"
            placeholder="https://example.com/job-posting"
            value={jobUrl}
            onChange={(e) => setJobUrl(e.target.value)}
          />

          {/* Analyze URL */}
          <button
            type="button"
            className="secondary-button"
            onClick={analyzeUrl}
            disabled={loading}
          >
            {loading ? "🔄 Analyzing..." : "🌐 Analyze URL"}
          </button>

          {/* History */}
          <button
            type="button"
            className="history-button"
            onClick={loadHistory}
            disabled={historyLoading}
          >
            {historyLoading
              ? "🔄 Loading History..."
              : "📊 View Analysis History"}
          </button>
        </section>

        {/* ====================================
            ANALYSIS RESULT
            ==================================== */}
        {result && (
          <section className="result-card">
            {/* Result Header */}
            <div className="result-header">
              <div>
                <p className="result-label">JOBSHIELD AI ANALYSIS</p>
                <h2>Security Assessment</h2>
              </div>

              <span className="analysis-complete">✓ Analysis Complete</span>
            </div>

            {/* =================================
                RISK SCORE
                ================================= */}
            <div
              className={`risk-box ${getRiskClass(
                result.risk_score,
                result.risk_level
              )}`}
            >
              <div className="risk-icon">
                {getRiskIcon(result.risk_score, result.risk_level)}
              </div>

              <div className="risk-info">
                <span className="risk-label">RISK LEVEL</span>

                <strong>{result.risk_level}</strong>

                <div className="risk-bar">
                  <div
                    className="risk-progress"
                    style={{
                      width: `${result.risk_score}%`,
                    }}
                  ></div>
                </div>
              </div>

              <div className="risk-score">
                <strong>{result.risk_score}</strong>
                <span>/100</span>
              </div>
            </div>

            {/* =================================
                RISK INDICATORS
                ================================= */}
            <div className="analysis-section">
              <div className="section-heading">
                <span>🚩</span>
                <h3>Risk Indicators</h3>
                <span className="count-badge">
                  {result.red_flags?.length || 0}
                </span>
              </div>

              {result.red_flags?.length === 0 ? (
                <div className="safe-message">
                  🟢 No major scam indicators detected.
                </div>
              ) : (
                <div className="flag-list">
                  {result.red_flags.map((flag, index) => (
                    <div className="flag-item" key={index}>
                      <div className="flag-content">
                        <span className="flag-icon">
                          {flag.points >= 20 ? "🔴" : "🟠"}
                        </span>

                        <div>
                          <strong>{flag.flag}</strong>
                          <small>Detection source: {flag.source}</small>
                        </div>
                      </div>

                      <span className="points">+{flag.points}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* =================================
                EMAIL ANALYSIS
                ================================= */}
            <div className="analysis-section">
              <div className="section-heading">
                <span>📧</span>
                <h3>Recruiter Verification</h3>
              </div>

              {result.emails?.length === 0 ? (
                <div className="info-message">
                  No email addresses were found in the posting.
                </div>
              ) : (
                <div className="email-list">
                  {result.emails.map((email, index) => (
                    <div className="email-item" key={index}>
                      <div>
                        <strong>{email.email}</strong>
                        <small>Domain: {email.domain}</small>
                      </div>

                      <span
                        className={
                          email.status === "SUSPICIOUS"
                            ? "status-danger"
                            : "status-safe"
                        }
                      >
                        {email.status === "SUSPICIOUS"
                          ? "⚠️ Suspicious"
                          : "✓ Company Domain"}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* =================================
                COMPANY VERIFICATION
                ================================= */}
            <div className="analysis-section">
              <div className="section-heading">
                <span>🏢</span>
                <h3>Company Verification</h3>
              </div>

              <div className="company-box">
                <div className="company-status">
                  <span>Status</span>

                  <strong
                    className={getCompanyStatusClass(
                      result.company_verification?.verification_status
                    )}
                  >
                    {result.company_verification?.verification_status ||
                      "UNKNOWN"}
                  </strong>
                </div>

                {result.company_verification?.company_name && (
                  <p>
                    Company:{" "}
                    <strong>{result.company_verification.company_name}</strong>
                  </p>
                )}

                <p>{result.company_verification?.explanation}</p>
              </div>
            </div>

            {/* =================================
                RECOMMENDATION
                ================================= */}
            <div className="recommendation">
              <div className="recommendation-icon">💡</div>

              <div>
                <h3>Safety Recommendation</h3>
                <p>{result.recommendation}</p>
              </div>
            </div>
          </section>
        )}

        {/* ====================================
            ANALYSIS HISTORY
            ==================================== */}
        {showHistory && (
          <section className="history-section">
            <div className="history-header">
              <div>
                <p className="result-label">JOBSHIELD AI</p>
                <h2>📊 Analysis History</h2>
                <p>Previous JobShield AI security assessments</p>
              </div>

              <button
                type="button"
                className="refresh-button"
                onClick={loadHistory}
                disabled={historyLoading}
              >
                {historyLoading ? "🔄 Refreshing..." : "🔄 Refresh"}
              </button>
            </div>

            {/* No History */}
            {history.length === 0 ? (
              <div className="empty-history">
                <div className="empty-icon">📭</div>
                <h3>No Analysis History</h3>
                <p>Your previous analyses will appear here.</p>
              </div>
            ) : (
              <div className="history-list">
                {history.map((item) => (
                  <div className="history-item" key={item.id}>
                    <div className="history-details">
                      <div className="history-company">
                        🏢 {item.company_name || "Unknown Company"}
                      </div>

                      <p>
                        {item.job_text?.length > 180
                          ? `${item.job_text.substring(0, 180)}...`
                          : item.job_text}
                      </p>

                      <small>
                        🕒{" "}
                        {item.created_at
                          ? new Date(item.created_at).toLocaleString()
                          : "Unknown date"}
                      </small>
                    </div>

                    <div
                      className={`history-score ${getRiskClass(
                        item.risk_score,
                        item.risk_level
                      )}`}
                    >
                      <strong>{item.risk_score}</strong>
                      <span>/100</span>
                      <small>{item.risk_level}</small>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}
      </main>

      {/* ======================================
          FOOTER
          ====================================== */}
      <footer>
        <p>🛡️ JobShield AI</p>
        <span>Protecting job seekers from fraudulent opportunities.</span>
      </footer>
    </div>
  );
}

export default App;