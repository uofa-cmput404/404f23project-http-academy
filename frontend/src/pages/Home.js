import React, { useState } from "react";
import Post from "../components/Post";
import "../css/Home.css"

export default function Home() {

    // TODO: replace these default test values with data from the backend
    const [posts, setPosts] = useState([{title: "Test", body: "Body"}]);

    const addPost = (title, body) => {
        setPosts([...posts, {title, body}]);
    };

    const postsChunks = posts.reduce((resultArray, item, index) => {
        const chunkIndex = Math.floor(index / 3);

        if (!resultArray[chunkIndex]) {
            resultArray[chunkIndex] = [];
        }

        resultArray[chunkIndex].push(item);

        return resultArray;
    }, []);

    return (
        <div className="posts-container">
            <h1>Home</h1>
            {postsChunks.map((chunk, chunkIndex) => (
                <div key={chunkIndex} className="posts-row">
                    {chunk.map((post, postIndex) => (
                        <Post key={postIndex} post={post}/>
                    ))}
                </div>
            ))}
            <button onClick={() => addPost("Test", "Body")}>Add Post</button>
        </div>
    );
}