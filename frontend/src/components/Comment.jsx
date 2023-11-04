import React from 'react';

export default function Comment({ comment, userid }) {
  console.log(comment)
  return (
    <div>
      
      <p> {userid} {comment}</p>
    </div>
  );
}