function FeatureChips() {

  const features = [
    "📄 Upload PDF",
    "📝 Summarize",
    "🔍 Research Topic",
    "📚 Citations",
    "📊 Analyze"
  ];

  return (

    <div className="chips">

      {features.map((item) => (

        <button
          key={item}
          className="chip"
        >
          {item}
        </button>

      ))}

    </div>

  );
}

export default FeatureChips;