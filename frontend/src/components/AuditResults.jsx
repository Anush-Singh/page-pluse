function AuditResults({ report }) {
  return (
    <section className="results-section">

      <div className="results-header">
        <div>
          <span className="section-label">
            AUDIT RESULTS
          </span>

          <h2>Page health overview</h2>
        </div>

        <a
          className="audited-url"
          href={report.url}
          target="_blank"
          rel="noreferrer"
        >
          {report.url}
        </a>
      </div>

      <div className="metrics-grid">

        <MetricCard
          label="HTTP Status"
          value={report.http_status}
        />

        <MetricCard
          label="Response Time"
          value={`${report.response_time_ms} ms`}
        />

        <MetricCard
          label="H1 Count"
          value={report.h1_count}
        />

        <MetricCard
          label="Missing Alt"
          value={report.images_missing_alt}
        />

        <MetricCard
          label="Word Count"
          value={report.word_count}
        />

      </div>

      <div className="page-details">

        <h2>Page Details</h2>

        <div className="detail-item">
          <span>Page Title</span>

          <p>
            {report.title || "No title found"}
          </p>
        </div>

        <div className="detail-item">
          <span>Meta Description</span>

          <p>
            {report.meta_description ||
              "No meta description found"}
          </p>
        </div>

      </div>

    </section>
  );
}

function MetricCard({ label, value }) {
  return (
    <div className="metric-card">

      <span className="metric-label">
        {label}
      </span>

      <strong className="metric-value">
        {value}
      </strong>

    </div>
  );
}

export default AuditResults;