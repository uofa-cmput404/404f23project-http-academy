import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import FriendRequestItem from '../components/FriendRequestItem';

describe('FriendRequestItem', () => {
  const mockRequest = {
    // 1 is the user_id of the user who sent the friend request
    actor: {
      user_id: '1',
      profileImage: 'test.jpg',
    },
    object: {
      user_id: '2',
    },
    type: 'Follow',
    accepted: false,
    summary: 'Test summary',
  };

  const mockConfirmFriendRequest = jest.fn();
  const mockEstablishMutualFriendship = jest.fn();

  it('renders without crashing', () => {
    // check if FriendRequestItem component renders without crashing
    render(<FriendRequestItem request={mockRequest} confirmFriendRequest={mockConfirmFriendRequest} establishMutualFriendship={mockEstablishMutualFriendship} />);
  });

  it('renders the correct content', () => {
    // check if FriendRequestItem component renders the correct content (summary)
    render(<FriendRequestItem request={mockRequest} confirmFriendRequest={mockConfirmFriendRequest} establishMutualFriendship={mockEstablishMutualFriendship} />);
    expect(screen.getByText(/Test summary/i)).toBeInTheDocument();
  });

  it('calls the correct function when Confirm button is clicked', () => {
    // check if FriendRequestItem component calls the correct function when Confirm button is clicked
    render(<FriendRequestItem request={mockRequest} confirmFriendRequest={mockConfirmFriendRequest} establishMutualFriendship={mockEstablishMutualFriendship} />);
    fireEvent.click(screen.getByText(/Confirm/i));
    expect(mockConfirmFriendRequest).toHaveBeenCalledWith('1', '2');
  });
});