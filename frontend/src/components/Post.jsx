import React from "react";
import "../css/Post.css"
import { Link } from 'react-router-dom'

export default function Post({ post }) {
    // TODO: Potentially move this into Post.css
    const neutral = {
        color: 'black',
        textDecoration: 'none'
    }

    return (
        <div className="card">
            <Link to={`/post/${post.id}`} style={neutral}>
            <div className="card-body">
                <h2 className="card-title">{post.title}</h2>
                <p className="card-text">{post.content}</p>
            </div>
          </Link>
        </div>
    );
}