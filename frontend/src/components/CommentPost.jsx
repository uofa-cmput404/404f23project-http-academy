import React, { useEffect, useState } from 'react';
import axiosInstance from '../axiosInstance';
import { Button, List, ListItem, ListItemText } from '@mui/material';
import '../css/SharePost.css';
import { extractUUIDFromURL } from '../utilities/extractUIID'
import Post from './Post';
import DetailedPost from './DetailedPost';

export default function SharePost({ posts, users }) {
    const storedUser_val = JSON.parse(localStorage.getItem('user'));
    const storedUser = storedUser_val.user
    const userId = storedUser.id.split("/").pop()
    const [selectedUserId, setSelectedUserId] = useState(null);
    const [post, setPost] = useState([]);
    const [allUsers, setAllusers] = useState([])

    const [postId, setPostId] = useState("")
    useEffect(() => {
        console.log('post in comment gotten from modal', posts.post_id);
        console.log('users in comment gotten from modal', users);
        const enrichedPosts = {
            ...post,
            authorDetails: findAuthorForPost(post.author)
        };
        setPost(enrichedPosts);
        setPostId(posts.post_id)
        // console.log('post id type', typeof posts.post_id)
        setAllusers(users)

    }, [posts, users]);


    const findAuthorForPost = (postId) => {
        return allUsers.find(user => user.id.includes(postId));
    };





    return (
        <div className='outer-container'>
            <DetailedPost post={post} id={postId} image={post.image} />
        </div>
    );
}

