function AuditForm({ url, setUrl, onSubmit, loading }) {
  return (
    <form className="audit-form" onSubmit={onSubmit}>
      <label htmlFor="website-url">
        Website URL
      </label>

      <div className="input-group">
        <input
          id="website-url"
          type="url"
          placeholder="https://example.com"
          value={url}
          onChange={(event) => setUrl(event.target.value)}
          required
          disabled={loading}
        />

        <button type="submit" disabled={loading}>
          {loading ? "Auditing..." : "Run Audit"}
        </button>
      </div>
    </form>
  );
}

export default AuditForm;