

import React, { useEffect, useState } from 'react';
import axiosInstance from '../axiosInstance';
import '../css/inbox.css';
import Post from '../components/Post';
import { extractUUIDFromURL } from '../utilities/extractUIID';

const Inbox = () => {
    const storedUser_val = JSON.parse(localStorage.getItem('user'));
    const storedUser = storedUser_val.user
    const userId = storedUser.id.split("/").pop()
    const [usersInboxItems, setUsersInboxItems] = useState([]);
    const [allUsers, setAllUsers] = useState([]);
    const [acceptedRequests, setAcceptedRequests] = useState({});
    const [followers, setFollowers] = useState([])

    useEffect(() => {
        getAllusers();
        getUsersInbox();
        fetchFollowers();
    }, []);

    const getAllusers = () => {
        axiosInstance.get('authors/user')
            .then(response => setAllUsers(response.data.items))
            .catch(error => console.log(error));
    };

    const getUsersInbox = () => {
        axiosInstance.get(`authors/${userId}/inbox/`)
            .then(response => {
                // Enrich posts with author details
                const enrichedPosts = response.data.posts.map(post => ({
                    ...post,
                    authorDetails: findAuthorForPost(post.author)
                }));

                setUsersInboxItems([...enrichedPosts, ...response.data.likes, ...response.data.follow_request]);
            })
            .catch(error => console.error('Error fetching inbox items:', error));
    };

    const findAuthorForPost = (postId) => {
        return allUsers.find(user => user.id.includes(postId));
    };

    const acceptFriendRequest = (requesterId, requestId) => {
        const url = `authors/${userId}/followers/acceptFriend/${requesterId}/`;
        axiosInstance.post(url, { user_id: userId, requesterId: requesterId })
            .then(() => {
                setAcceptedRequests({ ...acceptedRequests, [requestId]: true });

            })
            .catch(error => console.error('Error accepting friend request:', error));
    };

    const deleteFriendRequest = (requesterId, requestId) => {
        const url = `authors/${userId}/followers/acceptFriend/${requesterId}/`;
        axiosInstance.delete(url)
            .then(() => {
                // Update the state to remove the deleted request from the UI
                setUsersInboxItems(prevItems => prevItems.filter(item => item.id !== requestId));
            })
            .catch(error => console.error('Error deleting friend request:', error));
    };


    const fetchFollowers = (requestId) => {
        axiosInstance.get(`/authors/${userId}/followers`)
            .then(response => {
                setFollowers(response.data.items.map(item => extractUUIDFromURL(item.id)));
            })
            .catch(error => {
                console.error('Error fetching followers:', error);
            });


        // friendrequests/
        console.log('requester id', requestId)
        console.log('all followers', followers)
    };


    const Bidirectional = (friendId) => {
        console.log(' i went to bidirectional')
        const url = `authors/${userId}/followers/establishMutualFriendship/${friendId}/`
        axiosInstance.post(url, { user_id: userId, friendId: friendId })
            .then(() => getUsersInbox()) // Refresh inbox items after establishing mutual friendship
            .catch(error => console.error('Error establishing mutual friendship:', error));
    };



    const renderFriendRequest = (request) => {
        const requestId = request.id;
        const requesterId = extractUUIDFromURL(request.actor.id);
        const isAlreadyFollower = followers.includes(requesterId);
        const hasAcceptedRequest = acceptedRequests[requestId];

        return (
            <div key={requestId}>
                <p>{request.summary}</p>
                {!isAlreadyFollower && !hasAcceptedRequest && (
                    <button onClick={() => acceptFriendRequest(requesterId, requestId)}>
                        Accept
                    </button>
                )}
                {/* {!hasAcceptedRequest && (
                    <button onClick={() => deleteFriendRequest(requesterId, requestId)}>
                        Delete
                    </button>
                )} */}
                {(isAlreadyFollower || hasAcceptedRequest) && (
                    <button onClick={() => Bidirectional(requesterId)}>
                        Follow
                    </button>
                )}
            </div>
        );
    }


    const renderInboxItem = (item) => {
        switch (item.type) {
            case 'post':
                return <Post key={item.id} post={item} canEdit={userId === item.author} authorDetails={item.authorDetails} />;
            case 'Follow':
                return renderFriendRequest(item);

            default:
                return null;
        }
    };

    return (
        <div className='inbox-outer-container'>
            <h1>INBOX</h1>
            {usersInboxItems.map(renderInboxItem)}
        </div>
    );
};

export default Inbox;
