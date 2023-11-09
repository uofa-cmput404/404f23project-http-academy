import React from "react";
import "../css/DetailedPost.css";
import LikeButton from "../components/LikeButton";
import CommentSection from "./CommentSection";
import Markdown from 'react-markdown';

export default function DetailedPost({ post, id, image }) {
  const markdown = '# Hi, *Pluto*!';

  // If post content type is Markdown, use Markdown components. if not
  return (
    <div className="post">
      <div className="post-card">
        <h1 className="post-title">{post.title}</h1>
        <img src={`${image}`} alt="Base64" />
        <p className="post-text">{post.caption}</p>
        <LikeButton id={id} />
        {/* <DeleteButton id={id} /> */}
        <CommentSection comments={post.comments} />

        <Markdown>{markdown}</Markdown>
      </div>
    </div>
  );
}