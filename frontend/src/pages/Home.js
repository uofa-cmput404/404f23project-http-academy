import React, { useEffect, useState } from "react";
import Post from "../components/Post";
import "../css/Home.css";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import { useAuth } from "../context/AuthContext";
import { all } from "axios";

export default function Home() {
    const { isAuthenticated } = useAuth();
    let navigate = useNavigate();
    const [posts, setPosts] = useState([]);
    const [allUsers, setAllUsers] = useState([]);
    const storedUser = JSON.parse(localStorage.getItem('user'));
    const storedUser_str = storedUser.user
    const userId = storedUser_str.id.split("/").pop()
    useEffect(() => {
        if (!isAuthenticated) {
            navigate('/login'); // Redirect to login if not authenticated
        }
    }, [isAuthenticated, navigate]);

    useEffect(() => {
        axiosInstance.get('authors/user').then(response => {
            const usersWithProcessedIds = response.data.items.map(user => ({
                ...user
            }));
            setAllUsers(usersWithProcessedIds);
            console.log('goot it working', usersWithProcessedIds)

        }).catch(error => {
            console.log(error);
        });
    }, []); // Fetch all users

    useEffect(() => {
        const url = "authors/" + userId + "/posts/"
        axiosInstance.get('posts/').then(response => {
            const publicPosts = response.data.items.filter(p => p.visibility === "PUBLIC");
            const postsWithAuthors = publicPosts.map(post => ({
                ...post,
                authorDetails: findAuthorForPost(post)
            }));

            console.log('posts in home', postsWithAuthors)
            setPosts(postsWithAuthors);


        }).catch(error => {
            console.log(error);
        });
    }, [allUsers]); // Fetch posts after users are loaded



    // const extractIdFromUrl = (url) => {
    //     console.log('url sent ', url)
    //     const segments = url.split('/').pop();
    //     return segments
    // }

    const findAuthorForPost = (post) => {
        console.log('all users', allUsers);
        console.log('post', post);
        const found = allUsers.find(user => {
            const userId = user.id.split("/").filter(Boolean).pop();
            return userId === post.author;
        });
        console.log('found a user', found);
        return found;
    };

    const postsChunks = posts.reduce((resultArray, item, index) => {
        console.log('postng works', posts)
        const chunkIndex = Math.floor(index / 3);

        if (!resultArray[chunkIndex]) {
            resultArray[chunkIndex] = []; // Initialize a new chunk
        }

        resultArray[chunkIndex].push(item);
        return resultArray;
    }, []);

    return (
        <div className="posts-container">
            <h1>Explore</h1>
            {postsChunks.map((chunk, chunkIndex) => (
                <div key={chunkIndex} className="posts-row">
                    {chunk.map((post, postIndex) => (
                        <Post key={postIndex} post={post} canEdit={userId === post.author} authorDetails={post.authorDetails} />
                    ))}
                </div>
            ))}
        </div>
    );
}
