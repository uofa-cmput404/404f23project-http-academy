import React, { useEffect, useState } from "react";
import Post from "../components/Post";
import "../css/Home.css"
import { useNavigate } from "react-router-dom";
import axios from 'axios'
import PostService from '../services/posts'

export default function Home() {

    const [posts, setPosts] = useState([]);

    let navigate = useNavigate();

    useEffect(() => {
        PostService.getAll()
        .then(post => {
            setPosts(post)
        })
    }, [])

   
// import axiosInstance from "../axiosInstance";

// export default function Home() {

//     // TODO: fetch posts from backend
//     const defaultPosts = [
//         {title: "Test", body: "Body"},
//         {title: "Test", body: "Body"},
//         {title: "Test", body: "Body"},
//         {title: "Test", body: "Body"},
//     ];
//     const [posts, setPosts] = useState(defaultPosts);

//     // on page load, fetch posts from backend
//     useEffect(() => {
//         axiosInstance.get('posts/').then(response => {
//             console.log(response);
//             setPosts(response.data);
//         }).catch(error => {
//             console.log(error);
//         }
//         )}, []);


    const createPost = () => {
        navigate("/post/create");
    }



    // const postsChunks = posts.reduce((resultArray, item, index) => {
    //     const chunkIndex = Math.floor(index / 3);

    //     if (!resultArray[chunkIndex]) {
    //         resultArray[chunkIndex] = [];
    //     }

    //     resultArray[chunkIndex].push(item);

    //     return resultArray;
    // }, []);

    return (
        <div className="posts-container">
            <h1>Home</h1>
            {posts.map(post => (
                <div key={post.id} className="posts-row"> {/* key prop goes here */}
                    <Post post={post}/>
                </div>
            ))}
            <button onClick={createPost}>Add Post</button>
            <div className="square">
            </div>
        </div>
    );

}