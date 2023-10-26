import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axiosInstance from '../axiosInstance';
import Comment from './Comment';
// TODO: Add CSS 

export default function CommentSection() {
  const defaultComments = [
    { id: 1, author: 1, comment: "A comment" },
    { id: 2, author: 1, comment: "Another comment" },
    { id: 3, author: 1, comment: "One more comment" },
  ];
  const [comments, setComments] = useState(defaultComments);

  // Manage state of the textarea to clear it after an author posts a comment
  const [commentText, setCommentText] = useState('');

  const { id } = useParams();

  const addComment = (commentText) => {
    axiosInstance.post(`posts/${id}/comments/`, {
      postId: id,
      author: 1,
      comment: commentText
    }).then(response => {
      console.log(response);
      setComments([...comments, { id: response.data.id, author: 1, comment: commentText }]);
      setCommentText('');
    }).catch(error => {
      console.log(error);
    });
  };

  // Grab comments from the database
  useEffect(() => {
    axiosInstance.get(`posts/${id}/comments/`).then(response => {
      // console.log(response);
      setComments(response.data);
    }).catch(error => {
      console.log(error);
    });
  }, [id]);

  return (
    <div className='commentsection-container'>
      <h2>Comments</h2>
      {comments.map((comment) => (
        <Comment key={comment.id} comment={comment.comment} />
      ))}
      <textarea id="comment" name="comment" rows="2" cols="35" value={commentText} onChange={(e) => setCommentText(e.target.value)}></textarea>
      <button onClick={() => addComment(document.getElementById("comment").value)}>Post Comment</button>
    </div>
  );
}