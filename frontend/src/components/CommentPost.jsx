import React, { useEffect, useState, useCallback } from 'react';
import '../css/SharePost.css';
import DetailedPost from './DetailedPost';

export default function SharePost({ posts, users }) {
    const [post, setPost] = useState([]);
    const [allUsers, setAllusers] = useState([]);
    const [postId, setPostId] = useState("");


    const findAuthorForPost = useCallback((authorId) => {
        return allUsers.find(user => user.id.includes(authorId));
    }, [allUsers]);

    useEffect(() => {
        const enrichedPosts = {
            ...posts,
            authorDetails: findAuthorForPost(posts.author)
        };
        setPost(enrichedPosts);
        setPostId(posts.post_id);
        setAllusers(users);
    }, [posts, users, findAuthorForPost]); 

    return (
        <div className='outer-container'>
            <DetailedPost post={post} id={postId} image={post.image} />
        </div>
    );
}
