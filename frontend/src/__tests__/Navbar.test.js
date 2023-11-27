import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { useAuth } from '../context/AuthContext';
import { act } from 'react-dom/test-utils';

jest.mock('../context/AuthContext');

describe('Navbar', () => {
  // mock the logout function using jest
  const mockLogout = jest.fn();

  beforeEach(() => {
    // mock the logout function using jest before each test
    useAuth.mockReturnValue({
      logout: mockLogout,
    });
  });

  it('renders without crashing', () => {
    // check if Navbar component renders without crashing
    render(<MemoryRouter><Navbar /></MemoryRouter>);
  });

  it('renders the correct navigation links', () => {
    // check if Navbar component renders the correct navigation links
    render(<MemoryRouter><Navbar /></MemoryRouter>);
    expect(screen.getByText(/Home/i)).toBeInTheDocument();
    expect(screen.getByText(/Inbox/i)).toBeInTheDocument();
    expect(screen.getByText(/Hub/i)).toBeInTheDocument();
    expect(screen.getByText(/Profile/i)).toBeInTheDocument();
  });

  it('calls the logout function when "Logout" button is clicked', () => {
    // check if Navbar component calls the logout function when "Logout" button is clicked
    render(<MemoryRouter><Navbar /></MemoryRouter>);
    act(() => {
        fireEvent.click(screen.getByText(/Logout/i));
    });
    expect(mockLogout).toHaveBeenCalled();
  });
});