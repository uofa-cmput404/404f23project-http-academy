import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axiosInstance from '../axiosInstance';
import Comment from './Comment';
// Add CSS 

export default function CommentSection() {
  const defaultComments = [
    { id: 1, author: 1, comment: "A comment" },
    { id: 2, author: 1, comment: "Another comment" },
    { id: 3, author: 1, comment: "One more comment" },
  ];
  const [comments, setComments] = useState(defaultComments);
  const { id } = useParams();

  useEffect(() => {
    axiosInstance.get(`posts/${id}/comments/`).then(response => {
      // console.log(response);
      setComments(response.data);
    }).catch(error => {
      console.log(error);
    });
  }, []);

  return (
    <div className='commentsection-container'>
      <h2>Comments</h2>
      {comments.map((comment) => (
        <Comment key={comment.id} comment={comment.comment} />
      ))}
    </div>
  );
}