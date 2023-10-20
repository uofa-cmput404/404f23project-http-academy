import React from "react";
import "../css/Post.css"

export default function Post({ post }) {
    return (
        <div className="card-body">
            <h2 className="card-title">{post.title}</h2>
            <p className="card-text">{post.body}</p>
        </div>
    );
}