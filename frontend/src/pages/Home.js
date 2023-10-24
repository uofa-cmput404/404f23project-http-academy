import React, { useEffect, useState } from "react";
import Post from "../components/Post";
import "../css/Home.css";
import { useNavigate } from "react-router-dom";
import axios from 'axios'; 

export default function Home() {

    const [posts, setPosts] = useState([]);

    let navigate = useNavigate();

    useEffect(() => {
        axios.get('http://localhost:3001/posts')
        .then(response => {
            console.log('promise fulfilled')
            setPosts(response.data)
            console.log('here is my post', response.data)
        })
    }, []);

    const createPost = () => {
        navigate("/post/create");
    }

    return (
        <div className="posts-container">
            <h1>Home</h1>
            {posts.map(post => (
                <div key={post.id} className="posts-row">
                    <Post post={post}/>
                </div>
            ))}
            <button onClick={createPost}>Add Post</button>
            <div className="square">
            </div>
        </div>
    );
}
