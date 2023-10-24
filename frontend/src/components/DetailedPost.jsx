import React from "react";

export default function DetailedPost({ post }) {
  return (
    <div className="card">
      <div className="card-body">
        <h2 className="card-title">{post.title}</h2>
        <p className="card-text">{post.content}</p>
      </div> 
    </div>
  )
}