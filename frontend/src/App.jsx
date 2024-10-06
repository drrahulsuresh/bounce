import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      console.error("Error:", error);
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

      {response && (
        <div>
          <h2>Insights:</h2>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
