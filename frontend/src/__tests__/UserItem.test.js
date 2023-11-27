import React from 'react';
import { render, screen } from '@testing-library/react';
import UserItem from '../components/UserItem';

describe('UserItem', () => {
  // create a mock user
  const mockUser = {
    profileImage: 'test.jpg',
    displayName: 'TestUser',
  };

  it('renders without crashing', () => {
    // check if UserItem component renders without crashing
    render(<UserItem user={mockUser} />);
  });

  it('renders the correct image and display name', () => {
    // check if UserItem component renders the correct image and display name
    render(<UserItem user={mockUser} />);
    expect(screen.getByAltText(/Profile/i)).toHaveAttribute('src', 'test.jpg');
    expect(screen.getByText(/TestUser/i)).toBeInTheDocument();
  });
});