import React, { useEffect, useState } from 'react';
import '../css/SharePost.css';
import DetailedPost from './DetailedPost';

export default function SharePost({ posts, users }) {
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

    }, []);


    const findAuthorForPost = (postId) => {
        return allUsers.find(user => user.id.includes(postId));
    };





    return (
        <div className='outer-container'>
            <DetailedPost post={post} id={postId} image={post.image} />
        </div>
    );
}
