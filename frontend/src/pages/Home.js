import React, { useEffect, useState } from "react";
import Post from "../components/Post";
import "../css/Home.css";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import { useAuth } from "../context/AuthContext";
export default function Home() {

    const { isAuthenticated } = useAuth();
    let navigate = useNavigate();

    // TODO: fetch posts from backend
    const defaultPosts = [
        { title: "Test", body: "Body" },
        { title: "Test", body: "Body" },
        { title: "Test", body: "Body" },
        { title: "Test", body: "Body" },
    ];
    const [posts, setPosts] = useState(defaultPosts);

    // const { currentUser } = useAuth();

    const storedUser = JSON.parse(localStorage.getItem('user'));
    useEffect(() => {

        if (!isAuthenticated) {
            navigate('/login'); // Redirect to login if not authenticated
        }

    }, [isAuthenticated, navigate]);

    // on page load, fetch posts from backend
    useEffect(() => {

        axiosInstance.get('posts/').then(response => {

            const retrievePost = response.data;
            const publicPosts = retrievePost.filter(p => p.visibility === "PUBLIC");
            setPosts(publicPosts);
            console.log('checkig who made post', response.data);

        }).catch(error => {
            console.log(error);
        }
        );
    }, [isAuthenticated]);


    // useEffect(()=>{
    //     const storedUser = JSON.parse(localStorage.getItem('user'));
    //     if (storedUser.author === posts.author){
    //         setcanEdit(true)
    //     }
    // })

    // const createPost = () => {
    //     navigate("/post/create");
    // };

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
            <div>
                <h1>Explore</h1>
            </div>


            {/* {currentUser && <div>Welcome, {currentUser.username}!</div>} */}
            {postsChunks.map((chunk, chunkIndex) => (
                <div key={chunkIndex} className="posts-row">
                    {chunk.map((post, postIndex) => (

                        <Post key={postIndex} post={post} canEdit={storedUser.id === post.author} />
                    ))}
                </div>
            ))}
            {/* <button onClick={() => createPost()}>Add Post</button> */}
            <div className="square">
            </div>
        </div>
    );
}