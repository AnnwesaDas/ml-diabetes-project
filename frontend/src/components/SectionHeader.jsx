function SectionHeader({ eyebrow, title, description }) {
  return (
    <header className="section-header">
      {eyebrow ? <p className="section-eyebrow">{eyebrow}</p> : null}
      <h2>{title}</h2>
      {description ? <p>{description}</p> : null}
    </header>
  );
}

export default SectionHeader;
