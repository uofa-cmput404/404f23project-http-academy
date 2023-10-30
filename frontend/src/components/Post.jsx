import React, {useEffect, useState} from "react";
import "../css/Post.css"
import { Link } from 'react-router-dom'
import { useNavigate } from "react-router-dom";
export default function Post({ post, canEdit }) {

    console.log('edit prop', canEdit)
    let navigate = useNavigate();
    

  

    // Overrides the anchor tag styling caused by the Link component
    const neutral = {
        color: 'black',
        textDecoration: 'none'
    }

      //if the post is made by the current logged in user then display edit button 
  //else dont 
  
  
    
    const editPost = () => {
        
        console.log('can edit', canEdit)
        navigate(`/post/edit/${post.id}`);
    }
    

    return (
        <div className="card">
            <Link to={`/post/${post.id}`} style={neutral}>
            <div className="card-body">
                <h2 className="card-title">{post.title}</h2>
                <p className="card-text">{post.content}</p>
            </div>
           <h3>{canEdit}</h3>
          </Link>

            {canEdit ?  (
          <button onClick={editPost}>Edit</button> ): " "}
        </div>
    );
}
