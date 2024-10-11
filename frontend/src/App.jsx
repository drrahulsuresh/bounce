import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null); // New state for error handling

  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null); // Reset error state on new submission
    try {
      const res = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });
      if (!res.ok) {
        throw new Error(`Error: ${res.statusText}`);
      }
      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      setError(error.message); // Set error message
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>RAG Survey Insights</h1>
      <form onSubmit={handleQuerySubmit}>
        <input 
          type="text" 
          value={query} 
          onChange={(e) => setQuery(e.target.value)} 
          placeholder="Enter your query" 
          required 
        />
        <button type="submit">Submit Query</button>
      </form>

      {loading && <p>Loading...</p>}
      
      {error && <p className="error">{error}</p>} {/* Display error message */}
      
      {response && (
        <div>
          <h2>Insights:</h2>
          {/* Better formatted response display */}
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
