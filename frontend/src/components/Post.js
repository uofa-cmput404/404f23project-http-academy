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
                
                {post.contentType === 'image/png;base64' || post.contentType === 'image/jpeg;base64' ? 
                    <img src={`data:${post.contentType};base64,${post.content}`} alt={post.title} width = "200" height = "200"/> :
                    null
                }
                
                <p className="card-text">{post.description}</p>
                
                <button onClick={() => editPost()}>Edit</button>
            </div>
        </div>
    );
    
}
