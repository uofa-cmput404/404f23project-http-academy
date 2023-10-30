import React from 'react'
import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'
import Post from '../components/Post'
import ShallowRenderer from 'react-test-renderer/shallow';
import { BrowserRouter } from 'react-router-dom';

test('renders content', () => {
  const post = {
    title: 'Component testing is done with react-testing-library',
    content: 'testing the content'
  }

  const renderer = new ShallowRenderer()
  renderer.render(
    <BrowserRouter>
      <Post post={post} />
    </BrowserRouter>
  )
  const component = renderer.getRenderOutput()

  // expect the component page to contain text 'Component testing is done with react-testing-library'
  expect(component.props.children.props.post.title).toEqual('Component testing is done with react-testing-library')
})