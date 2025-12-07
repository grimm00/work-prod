/**
 * Tests for HealthCheck Component
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import HealthCheck from './HealthCheck';
import api from '../services/api';

// Mock the api module
vi.mock('../services/api');

describe('HealthCheck', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks();
  });

  it('renders loading state initially', () => {
    // Mock API to never resolve
    api.get.mockImplementation(() => new Promise(() => {}));
    
    render(<HealthCheck />);
    expect(screen.getByText('Checking backend connection...')).toBeInTheDocument();
  });

  it('renders success message when API call succeeds', async () => {
    // Mock successful API response
    api.get.mockResolvedValue({
      data: {
        status: 'ok',
        message: 'Flask backend is running'
      }
    });

    render(<HealthCheck />);

    await waitFor(() => {
      expect(screen.getByText('✓ Flask backend is running')).toBeInTheDocument();
    });
  });

  it('renders error message when API call fails', async () => {
    // Mock API error
    api.get.mockRejectedValue(new Error('Network error'));

    render(<HealthCheck />);

    await waitFor(() => {
      expect(screen.getByText(/Error: Network error/)).toBeInTheDocument();
    });
  });

  it('calls the health endpoint on mount', async () => {
    // Mock successful API response
    api.get.mockResolvedValue({
      data: {
        status: 'ok',
        message: 'Flask backend is running'
      }
    });

    render(<HealthCheck />);

    await waitFor(() => {
      expect(api.get).toHaveBeenCalledWith('/health');
      expect(api.get).toHaveBeenCalledTimes(1);
    });
  });
});

