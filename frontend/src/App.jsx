import React, { useState } from 'react';
import InsightsChart from './Insights';

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [chartData, setChartData] = useState([]);

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

      // Truncate the response to a specific length
      const truncatedResponse = data.response.length > 300
        ? data.response.substring(0, 300) + "..."
        : data.response;

      setResponse(truncatedResponse);

      // Example logic for setting chart data based on query
      const parsedData = [65, 59, 80]; // Modify this based on actual response data
      setChartData(parsedData);

    } catch (error) {
      console.error("Error:", error);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <div className="form-container">
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

        {loading && <p className="loading">Loading...</p>}

        {response && (
          <div className="response-container">
            <h2>Insights:</h2>
            <pre>{response}</pre>

            {/* Only show the chart when response is available */}
            {chartData.length > 0 && <InsightsChart data={chartData} />}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
