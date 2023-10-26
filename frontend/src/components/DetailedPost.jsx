import React from "react";
import "../css/DetailedPost.css";
import LikeButton from "../components/LikeButton";
import DeleteButton from "../components/DeleteButton";
import CommentSection from "./CommentSection";

export default function DetailedPost({ post, id, image }) {
  return (
    <div className="post">
      <div className="post-card">
        <h1 className="post-title">{post.title}</h1>
        <img src={`${image}`} alt="Base64 Image" />
        <p className="post-text">{post.caption}</p>
        <LikeButton id={id} />
        <DeleteButton id={id} />
        <CommentSection comments={post.comments} />
      </div>
    </div>
  );
}