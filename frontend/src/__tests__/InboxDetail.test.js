import React from 'react';
import { render, screen } from '@testing-library/react';
import InboxDetail from '../components/InboxDetail';

describe('InboxDetail', () => {
  const mockItemLike = {
    type: 'Like',
    author: {
      profileImage: 'test.jpg',
    },
    summary: 'Test summary',
  };

  const mockItemFollow = {
    type: 'Follow',
    profileImage: 'test.jpg',
    summary: 'Test summary',
  };

  it('renders without crashing', () => {
    render(<InboxDetail item={mockItemLike} />);
  });

  it('renders the correct content for Like type', () => {
    render(<InboxDetail item={mockItemLike} />);
    expect(screen.getByText(/Test summary/i)).toBeInTheDocument();
    expect(screen.getByAltText(/Preview/i)).toBeInTheDocument();
  });

  it('renders the correct content for Follow type', () => {
    render(<InboxDetail item={mockItemFollow} />);
    expect(screen.getByText(/Test summary/i)).toBeInTheDocument();
    expect(screen.getByAltText(/Preview/i)).toBeInTheDocument();
  });
});