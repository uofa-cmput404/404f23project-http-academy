import React from 'react';
import { render, screen } from '@testing-library/react';
import Comment from '../components/Comment';

describe('Comment', () => {
  it('renders without crashing', () => {
    // check if Comment component renders without crashing
    render(<Comment comment="Test comment" userid="TestUser" />);
  });

  it('renders the correct content', () => {
    // check if Comment component renders the correct content (comment and userid)
    render(<Comment comment="Test comment" userid="TestUser" />);
    expect(screen.getByText(/TestUser/i)).toBeInTheDocument();
    expect(screen.getByText(/Test comment/i)).toBeInTheDocument();
  });
});