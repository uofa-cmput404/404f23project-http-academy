// Post.js
import React from "react";
import "../css/Post.css";
import { useNavigate } from "react-router-dom";

export default function Post({ post }) {

    let navigate = useNavigate();
    
    const editPost = () => {
        // console.log('here is the post clicked on', post)
        navigate(`/post/edit/${post.id}`);
    }
    
    return (
        <div className="card">
            <div className="card-body">
                
                <h2 className="card-title">{post.title}</h2>
                <p className="card-text">{post.body}</p>
                <button onClick={() => editPost()}>Edit</button>
            </div>
        </div>
    );
}
