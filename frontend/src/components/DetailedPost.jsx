import React from "react";
import "../css/DetailedPost.css";
import LikeButton from "../components/LikeButton";
import CommentSection from "./CommentSection";

export default function DetailedPost({ post, id, image }) {
  return (
    <div className="post">
      <div className="post-card">
        <h1 className="post-title">{post.title}</h1>
        {image ? <img src={`${image}`} alt="Base64" /> : ""}
        <p className="post-text">{post.content}</p>
        <LikeButton id={id} />
        <CommentSection comments={post.comments} />
      </div>
    </div>
  );
}