import { useState } from "react";

import AuditForm from "./components/AuditForm";
import AuditResults from "./components/AuditResults";

import "./App.css";
const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";
function App() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");


  async function handleAudit(event) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setReport(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/audit",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            url: url,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        let message = "Unable to audit this website.";

        if (typeof data.detail === "string") {
          message = data.detail;
        }

        throw new Error(message);
      }

      setReport(data);

    } catch (err) {
      setError(
        err.message || "Something went wrong."
      );

    } finally {
      setLoading(false);
    }
  }


  return (
    <div className="app">
      <main>
        <section className="hero">
          <span className="eyebrow">
            WEBSITE HEALTH AUDIT
          </span>

          <h1>Page Pulse</h1>

          <p>
            Enter any public webpage to check its
            HTTP response, metadata, headings and
            accessibility basics.
          </p>

          <AuditForm
            url={url}
            setUrl={setUrl}
            onSubmit={handleAudit}
            loading={loading}
          />

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          {report && (
  <AuditResults report={report} />
)}
        </section>
      </main>
      <footer className="footer">
  Built for Digital Heroes Training Task
     </footer>
    </div>
  );
}

export default App;