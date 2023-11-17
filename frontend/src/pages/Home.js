import React, { useEffect, useState } from "react";
import Post from "../components/Post";
import "../css/Home.css";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import { useAuth } from "../context/AuthContext";

export default function Home() {
    const { isAuthenticated } = useAuth();
    let navigate = useNavigate();
    const [posts, setPosts] = useState([]);
    const [allUsers, setAllUsers] = useState([]);
    const storedUser = JSON.parse(localStorage.getItem('user'));

    useEffect(() => {
        if (!isAuthenticated) {
            navigate('/login'); // Redirect to login if not authenticated
        }
    }, [isAuthenticated, navigate]);

    useEffect(() => {
        axiosInstance.get('authors/user').then(response => {
            const usersWithProcessedIds = response.data.items.map(user => ({
                ...user,
                numericId: extractIdFromUrl(user.id)
            }));
            setAllUsers(usersWithProcessedIds);
            console.log('goot it working', response.data.items)
            
        }).catch(error => {
            console.log(error);
        });
    }, []); // Fetch all users

    useEffect(() => {
        axiosInstance.get('posts/').then(response => {
            const publicPosts = response.data.filter(p => p.visibility === "PUBLIC");
            const postsWithAuthors = publicPosts.map(post => ({
                ...post,
                authorDetails: findAuthorForPost(post)
            }));
            
            setPosts(postsWithAuthors);
            
        
        }).catch(error => {
            console.log(error);
        });
    }, [allUsers]); // Fetch posts after users are loaded

    

    const extractIdFromUrl = (url) => {
        const segments = url.split('/');
        return segments[segments.length - 1];
    }

    const findAuthorForPost = (post) => {
        return allUsers.find(user => user.numericId === post.author.toString());
    }

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
                        <Post key={postIndex} post={post} canEdit={storedUser.id === post.author} authorDetails={post.authorDetails} />
                    ))}
                </div>
            ))}
        </div>
    );
}
