import React from 'react';
import { render, screen } from '@testing-library/react';
import UserItem from '../components/UserItem';

describe('UserItem', () => {
  const mockUser = {
    profileImage: 'test.jpg',
    displayName: 'TestUser',
  };

  it('renders without crashing', () => {
    render(<UserItem user={mockUser} />);
  });

  it('renders the correct image and display name', () => {
    render(<UserItem user={mockUser} />);
    expect(screen.getByAltText(/Profile/i)).toHaveAttribute('src', 'test.jpg');
    expect(screen.getByText(/TestUser/i)).toBeInTheDocument();
  });
});