import React from "react";
import "../css/Post.css"
import { Link } from 'react-router-dom'
import { useNavigate } from "react-router-dom";
export default function Post({ post }) {

    let navigate = useNavigate();
    

    // Overrides the anchor tag styling caused by the Link component
    const neutral = {
        color: 'black',
        textDecoration: 'none'
    }

    const editPost = () => {
        console.log('here is the post clicked on', post)
        navigate(`/post/edit/${post.id}`);
    }
    

    return (
        <div className="card">
            <Link to={`/post/${post.id}`} style={neutral}>
            <div className="card-body">
                <h2 className="card-title">{post.title}</h2>
                <p className="card-text">{post.content}</p>
            </div>
           
          </Link>
          <button onClick={editPost}>Edit</button>
        </div>
    );
}