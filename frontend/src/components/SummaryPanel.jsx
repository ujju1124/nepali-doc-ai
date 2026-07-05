function SummaryPanel({ summaries }) {
  return (
    <div className="summary-section">
      <h3 className="section-title">What This Document Says</h3>
      
      <div className="summary-cards">
        {/* English Summary */}
        <div className="summary-card">
          <h4 className="summary-card-title">English Summary</h4>
          <p className="summary-text english">
            {summaries.english_summary}
          </p>
        </div>

        {/* Nepali Summary */}
        <div className="summary-card">
          <h4 className="summary-card-title">Nepali Summary</h4>
          <p className="summary-text nepali">
            {summaries.nepali_summary}
          </p>
        </div>
      </div>

      {/* Key Facts */}
      <div className="key-facts-section">
        <h4 className="key-facts-title">Key Facts</h4>
        <ol className="key-facts-list">
          {summaries.key_facts.map((fact, index) => (
            <li key={index} className="key-fact-item">
              {fact}
            </li>
          ))}
        </ol>
      </div>
    </div>
  )
}

export default SummaryPanel
