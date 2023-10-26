import React from "react";
import "../css/DetailedPost.css"

export default function DetailedPost({ post }) {
  return (
    <div className="post">
      <div className="post-card">
        <h2 className="post-title">{post.title}</h2>
        <p className="post-text">{post.content}</p>
      </div> 
    </div>
  )
}