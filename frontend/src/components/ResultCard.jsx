function ResultCard({ label, value, tone = 'neutral', helper }) {
  return (
    <article className={`result-card ${tone}`}>
      <p className="result-label">{label}</p>
      <h3>{value}</h3>
      {helper ? <p className="result-helper">{helper}</p> : null}
    </article>
  );
}

export default ResultCard;
