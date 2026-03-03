import { useState } from 'react'
import './index.css'
import SearchForm from './components/SearchForm'
import FareTable from './components/FareTable'

function App() {
  const [fareData, setFareData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchFares = async (searchParams) => {
    setLoading(true);
    setError(null);
    try {
      // Build query string
      const params = new URLSearchParams(searchParams);
      const response = await fetch(`http://localhost:8000/api/fares?${params}`);

      if (!response.ok) {
        throw new Error('Failed to fetch fare data. Please check your inputs or try again later.');
      }

      const result = await response.json();

      if (result.status === 'success' && result.data && result.data.resultObject) {
        setFareData(result.data.resultObject.graphData || []);
      } else {
        throw new Error('No data returned from the server.');
      }
    } catch (err) {
      setError(err.message);
      setFareData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <header className="header">
        <h1>crawl-surff</h1>
        <p>Real-time fare tracking for major routes</p>
      </header>

      <main>
        <div className="glass-panel">
          <SearchForm onSearch={fetchFares} isLoading={loading} />

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
        </div>

        {fareData !== null && !error && (
          <div className="glass-panel results-container">
            <div className="results-header">
              <h2>Fare Trends</h2>
            </div>

            {fareData.length > 0 ? (
              <FareTable data={fareData} />
            ) : (
              <div className="empty-state">
                <p>No fare data found for this route.</p>
              </div>
            )}
          </div>
        )}
      </main>
    </>
  )
}

export default App
