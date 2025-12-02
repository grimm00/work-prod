/**
 * HealthCheck Component
 * 
 * Verifies backend connectivity by calling the /api/health endpoint.
 * Displays loading, success, or error states.
 */

import { useState, useEffect } from 'react';
import api from '../services/api';

function HealthCheck() {
  const [status, setStatus] = useState('loading');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await api.get('/health');
        setStatus('success');
        setMessage(response.data.message);
      } catch (err) {
        setStatus('error');
        setError(err.message || 'Failed to connect to backend');
      }
    };

    checkHealth();
  }, []);

  if (status === 'loading') {
    return (
      <div className="health-check">
        <p>Checking backend connection...</p>
      </div>
    );
  }

  if (status === 'error') {
    return (
      <div className="health-check error">
        <p>Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="health-check success">
      <p>✓ {message}</p>
    </div>
  );
}

export default HealthCheck;

