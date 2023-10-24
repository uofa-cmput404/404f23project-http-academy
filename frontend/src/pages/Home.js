import React, { useEffect, useState } from "react";
import Post from "../components/Post";
import "../css/Home.css"
import { useNavigate } from "react-router-dom";
import axios from 'axios'

export default function Home() {

    // TODO: fetch posts from backend
    // const defaultPosts = [
    //     {title: "Test", body: "Body", id: 1},
    //     {title: "Test", body: "Body", id: 2},
    //     {title: "Test", body: "Body", id: 3},
    //     {title: "Test", body: "Body", id: 4},
    // ];

    const [posts, setPosts] = useState([]);

    let navigate = useNavigate();

    useEffect(() => {
        axios.get('http://localhost:3001/posts')
        .then(response => {
            console.log('promise fulfilled')
            setPosts(response.data)
            console.log('here is my post', response.data)
        })
    }, [])

   


    const createPost = () => {
        navigate("/post/create");
    }

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
    

    // const postsChunks = posts.reduce((resultArray, item, index) => {
    //     const chunkIndex = Math.floor(index / 3);

    //     if (!resultArray[chunkIndex]) {
    //         resultArray[chunkIndex] = [];
    //     }

    //     resultArray[chunkIndex].push(item);

    //     return resultArray;
    // }, []);

    // return (
    //     <div className="posts-container">
    //         <h1>Home</h1>
    //         {/* {posts.map((chunk, chunkIndex) => (
    //             <div key={chunkIndex} className="posts-row">
    //                 {chunk.map((post, postIndex) => (
    //                     <Post key={postIndex} post={post}/>
    //                 ))}
    //             </div>
    //         ))} */}
    //         {posts.map((post) => {
    //             <Post key = {post.id} post = {post}/>
    //         })}
    //         <button onClick={() => createPost()}>Add Post</button>
    //         <div className="square">
    //         </div>
    //     </div>
    // );

}