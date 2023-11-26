import React, { useEffect, useState, useCallback } from 'react';
import axiosInstance from '../axiosInstance';
import { Button, List, ListItem, ListItemText } from '@mui/material';
import '../css/Hub.css';
// import { extractUUIDFromURL } from '../utilities/extractUIID';

export default function Hub() {
    const loggedINUser = JSON.parse(localStorage.getItem('user'));
    const storedUser = loggedINUser?.user;
    const userId = storedUser?.id.split("/").pop();

    const [allUsers, setAllUsers] = useState([]);

    const [sentRequests, setSentRequests] = useState(new Set());

    const [followingList, setFollowingList] = useState([])
    // const [followersList, setFollowersList] = useState([])

    // const [isFollowingLoaded, setIsFollowingLoaded] = useState(false);
    const [isFollowersLoaded, setIsFollowersLoaded] = useState(false);


    const extractUUIDFromURL = (url) => {
        const parts = url.split('/');
        let uuid = parts.pop() || parts.pop();
        return uuid;
    };

    const fetchAllUsers = useCallback(() => {
        axiosInstance.get("authors/user")
            .then(response => {
                const filteredUsers = response.data.items.filter(item => {
                    const userUUID = extractUUIDFromURL(item.id);
                    return userUUID !== userId && !followingList.includes(userUUID);
                });
                setAllUsers(filteredUsers);
            })
            .catch(error => console.error('Error fetching users:', error));
    }, [userId, followingList]);

    const fetchFollowing = useCallback(() => {
        axiosInstance.get(`/authors/${userId}/following`)
            .then(response => {
                setFollowingList(response.data.items.map(item => extractUUIDFromURL(item.id)));
            })
            .catch(error => console.error('Error fetching following:', error));
    }, [userId]);

    const fetchFollowers = useCallback(() => {
        axiosInstance.get(`/authors/${userId}/followers`)
            .then(response => {
                // setFollowersList(response.data.items.map(item => extractUUIDFromURL(item.id)));
                setIsFollowersLoaded(true);
            })
            .catch(error => console.error('Error fetching followers:', error));
    }, [userId]);

    const fetchSentFriendRequests = useCallback(() => {
        axiosInstance.get(`authors/${userId}/followers/sentFriendRequests/`)
            .then(response => {
                const requests = new Set(response.data.map(req => extractUUIDFromURL(req.object.id)));
                setSentRequests(requests);
            })
            .catch(error => console.error('Error fetching sent friend requests:', error));
    }, [userId]);

    useEffect(() => {
        fetchFollowing();
        fetchFollowers();
    }, [userId, fetchFollowing, fetchFollowers]);

    useEffect(() => {
        if (isFollowersLoaded) {
            fetchAllUsers();
        }
    }, [isFollowersLoaded, fetchAllUsers, followingList, sentRequests]);

    useEffect(() => {
        fetchSentFriendRequests();
    }, [userId, fetchSentFriendRequests]);

    const handleFollow = (user) => {
        const followData = {
            type: "Follow",
            summary: `${storedUser.displayName} sent you a friend request.`,
            object: {
                type: "follow",
                id: user.url,
                host: user.host,
                displayName: user.displayName,
                url: user.url,
                github: user.github,
                profileImage: user.profileImage
            },
            actor: {
                ...storedUser
            }
        };

        const userUUID = extractUUIDFromURL(user.id);

        axiosInstance.post(`authors/${userUUID}/inbox/`, followData)
            .then(response => {
                setSentRequests(new Set([...sentRequests, userUUID])); // Update the state

                console.log("Friend request sent", response);
                // setButtonState('Request Sent')
            })

            .catch(error => console.error('Error sending friend request:', error));
    };



    // const getButtonState = (userUUID) => {
    //     if (!followingList.includes(userUUID)) {
    //         return 'Follow';
    //     } else if (sentRequests.has(userUUID)) {
    //         return 'Request Sent';
    //     }
    // };

    // const getdisabledState = (userUUID) => {
    //     if (!followingList.includes(userUUID)) {
    //         return false;
    //     } else if (sentRequests.has(userUUID)) {
    //         return true;
    //     }
    // };


    return (
        <div className='outer-containers2'>
            <div className='full-contains2'>
                <h1 className='header'>HUB</h1>
                <h4>Looking for someone new to follow!</h4>
            </div>
            <div className='list-flexs2'>
                <List>
                    {allUsers.map((user) => {
                        const userUUID = extractUUIDFromURL(user.id);
                        const isRequestSent = sentRequests.has(userUUID);
                        const buttonLabel = isRequestSent ? 'Request Sent' : 'Follow';
                        const disabledState = isRequestSent;

                        return (
                            <ListItem key={user.id}>
                                <ListItemText primary={user.displayName} />
                                <Button
                                    variant="outlined"
                                    onClick={() => handleFollow(user)}
                                    disabled={disabledState}
                                >
                                    {buttonLabel}
                                </Button>
                            </ListItem>
                        );
                    })}

                </List>
            </div>
        </div>
    );
}
