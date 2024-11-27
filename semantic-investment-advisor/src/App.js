import React, { useState } from "react";
import "./App.css"; // Import CSS styles

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [filters, setFilters] = useState({
    investment_type: "",
    sector: "",
    industry: "",
    risk_level: "",
    timeframe: "",
  });

  const handleSearch = async () => {
    const response = await fetch("http://localhost:5000/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, filters }),
    });
    const data = await response.json();
    setResults(data);
  };

  return (
    <div className="app-container">
      <h1 className="app-title">Semantic Investment Advisor</h1>
      <div className="search-container">
        <input
          type="text"
          className="search-input"
          placeholder="Enter your query (e.g., Low-risk investments for retirement)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <div className="filter-group">
          <select
            className="filter-select"
            onChange={(e) =>
              setFilters({ ...filters, investment_type: e.target.value })
            }
          >
            <option value="">Investment Type</option>
            <option value="Stock">Stock</option>
          </select>
          <select
            className="filter-select"
            onChange={(e) => setFilters({ ...filters, sector: e.target.value })}
          >
            <option value="">Sector</option>
            <option value="Technology">Technology</option>
            <option value="Trade & services">Trade & Services</option>
            <option value="Manufacturing">Manufacturing</option>
          </select>
          <select
            className="filter-select"
            onChange={(e) =>
              setFilters({ ...filters, industry: e.target.value })
            }
          >
            <option value="">Industry</option>
            <option value="Electronic computers">Electronic Computers</option>
            <option value="Services-prepackaged software">
              Services - Prepackaged Software
            </option>
            <option value="Retail-catalog & mail-order houses">
              Retail - Catalog & Mail Order Houses
            </option>
          </select>
          <select
            className="filter-select"
            onChange={(e) =>
              setFilters({ ...filters, risk_level: e.target.value })
            }
          >
            <option value="">Risk Level</option>
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>
          <select
            className="filter-select"
            onChange={(e) =>
              setFilters({ ...filters, timeframe: e.target.value })
            }
          >
            <option value="">Timeframe</option>
            <option value="Short-term">Short-term</option>
            <option value="Long-term">Long-term</option>
          </select>
        </div>
        <button className="search-button" onClick={handleSearch}>
          Search
        </button>
      </div>
      <div className="results-container">
        <h2 className="results-title">Results:</h2>
        {results.length > 0 ? (
          results.map((result, index) => (
            <div key={index} className="result-card">
              <h3 className="result-name">{result.name}</h3>
              <p className="result-description">{result.description}</p>
              <p className="result-score">Score: {result.score.toFixed(2)}</p>
              <div className="result-meta">
                <p>Sector: {result.sector}</p>
                <p>Industry: {result.industry}</p>
                <p>Risk Level: {result.risk_level}</p>
                <p>Timeframe: {result.timeframe}</p>
              </div>
            </div>
          ))
        ) : (
          <p>No results found</p>
        )}
      </div>
    </div>
  );
}

export default App;
