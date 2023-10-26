import React from "react";
import "../css/DetailedPost.css";
import LikeButton from "../components/LikeButton";
import DeleteButton from "../components/DeleteButton";

export default function DetailedPost({ post, id }) {
  return (
    <div className="post">
      <div className="post-card">
        <h2 className="post-title">{post.title}</h2>
        <p className="post-text">{post.content}</p>
        <LikeButton id={id} />
        <DeleteButton id={id} />
      </div>
    </div>
  );
}