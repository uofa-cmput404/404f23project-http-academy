import React, { useEffect, useState, useCallback } from "react";
import Post from "../components/Post";
import "../css/Home.css";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import { useAuth } from "../context/AuthContext";
import GitHubPost from "../components/GithubPost";
import Search from "../components/Search";
// import { all } from "axios";

export default function Home() {
    const { isAuthenticated } = useAuth();
    let navigate = useNavigate();
    const [posts, setPosts] = useState([]);
    const [allUsers, setAllUsers] = useState([]);
    const storedUser = JSON.parse(localStorage.getItem('user'));
    const storedUser_str = storedUser.user;
    const userId = storedUser_str.id.split("/").pop();
    const [githubUrl, setGithubUrl] = useState('');
    const [oldPosts, setOldPosts] = useState([]);

    useEffect(() => {

        if (!isAuthenticated) {
            navigate('/login'); // Redirect to login if not authenticated
        }
    }, [isAuthenticated, navigate, storedUser]);

    useEffect(() => {
        // Fetch all users
        const githubUrl = storedUser_str.github;
        setGithubUrl(githubUrl);
        // console.log('all users ', storedUser_str);
        axiosInstance.get('authors/user').then(response => {
            const usersWithProcessedIds = response.data.items.map(user => ({
                ...user
            }));
            setAllUsers(usersWithProcessedIds);
        }).catch(error => {
            console.log(error);
        });
    }, []);

    // const extractIdFromUrl = (url) => {
    //     console.log('url sent ', url)
    //     const segments = url.split('/').pop();
    //     return segments
    // }

    const findAuthorForPost = useCallback((post) => {
        const found = allUsers.find(user => {
            const userId = user.id.split("/").filter(Boolean).pop();
            return userId === post.author;
        });
        return found;
    }, [allUsers]);

    useEffect(() => {
        // Fetch posts after users are loaded
        axiosInstance.get('posts/').then(response => {
            const publicPosts = response.data.items.filter(p => p.visibility === "PUBLIC");
            const postsWithAuthors = publicPosts.map(post => ({
                ...post,
                authorDetails: findAuthorForPost(post)
            }));
            setPosts(postsWithAuthors);
            setOldPosts(postsWithAuthors);
        }).catch(error => {
            console.log(error);
        });
    }, [allUsers, findAuthorForPost]);


    const postsChunks = posts.reduce((resultArray, item, index) => {
        // console.log('postng works', posts);
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
            <Search setPosts={setPosts} findAuthorForPost={findAuthorForPost} oldPosts={oldPosts} />
            {githubUrl && < GitHubPost githubUrl={githubUrl} className="posts-row" />}
            {posts.length === 0 ? (
                <p>No posts found.</p>
            ) : (
                postsChunks.map((chunk, chunkIndex) => (
                    <div key={chunkIndex} className="posts-row">
                        {chunk.map((post, postIndex) => (
                            <Post key={postIndex} post={post} canEdit={userId === post.author} authorDetails={post.authorDetails} />
                        ))}
                    </div>
                ))
            )}

        </div>
    );
}