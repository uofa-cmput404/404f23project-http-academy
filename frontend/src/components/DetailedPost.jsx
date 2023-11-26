import React from "react";
import "../css/DetailedPost.css";
import CommentSection from "./CommentSection";

export default function DetailedPost({ post, id, image }) {
  return (
    <div>
      <div>
        {/* <h1 className="post-title">{post.title}</h1> */}
        {/* <img src={`${image}`} alt="Base64" /> */}
        <p className="post-text">{post.caption}</p>
        {/* <LikeButton id={id} /> */}
        {/* <DeleteButton id={id} /> */}
        <CommentSection postid={id} />
      </div>
    </div>
  );
}
