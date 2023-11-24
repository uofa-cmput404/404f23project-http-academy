import React, { useEffect, useState } from 'react';
import axiosInstance from '../axiosInstance';
import { Button, List, ListItem, ListItemText } from '@mui/material';
import '../css/Hub.css';
// import { extractUUIDFromURL } from '../utilities/extractUIID';

export default function Hub() {
    const loggedINUser = JSON.parse(localStorage.getItem('user'));
    const storedUser = loggedINUser?.user;
    const userId = storedUser?.id.split("/").pop();

    const [allUsers, setAllUsers] = useState([]);
    const [followRequests, setFollowRequests] = useState({});
    const [sentRequests, setSentRequests] = useState(new Set());

    const [followingList, setFollowingList] = useState([])
    const [followersList, setFollowersList] = useState([])

    const [isFollowingLoaded, setIsFollowingLoaded] = useState(false);
    const [isFollowersLoaded, setIsFollowersLoaded] = useState(false);

    const [buttonState, setButtonState] = useState("Follow")
    useEffect(() => {
        fetchFollowing();
        fetchFollowers();
    }, [userId]);

    useEffect(() => {
        if (isFollowersLoaded) {
            fetchAllUsers();
        }



    }, [followingList, sentRequests]);

    useEffect(() => {
        fetchSentFriendRequests();
    }, [userId]);


    const extractUUIDFromURL = (url) => {
        const parts = url.split('/');
        let uuid = parts.pop() || parts.pop();
        return uuid;
    };


    const fetchAllUsers = () => {
        axiosInstance.get("authors/user")
            .then(response => {
                // Filter out users that are already being followed
                const filteredUsers = response.data.items.filter(item => {
                    const userUUID = extractUUIDFromURL(item.id);
                    console.log('foollowig list', followingList)
                    console.log('fellowers list', followersList)
                    console.log('user id', userUUID)
                    console.log('other user id', userId)
                    return userUUID !== userId && !followingList.includes(userUUID);
                });
                console.log('filters user showing', filteredUsers)
                setAllUsers(filteredUsers);
            })
            .catch(error => console.error('Error fetching users:', error));
    };

    const fetchFollowing = (requestId) => {
        axiosInstance.get(`/authors/${userId}/following`)
            .then(response => {
                setFollowingList(response.data.items.map(item => extractUUIDFromURL(item.id)));
                setIsFollowingLoaded(true);
            })
            .catch(error => {
                console.error('Error fetching followers:', error);
            });
        console.log('requester id', requestId)
        console.log('all following', followingList)
    };

    const fetchFollowers = (requestId) => {
        axiosInstance.get(`/authors/${userId}/followers`)
            .then(response => {
                console.log('ogo foll', response.data.items)
                setFollowersList(response.data.items.map(item => extractUUIDFromURL(item.id)));
                setIsFollowersLoaded(true);
            })
            .catch(error => {
                console.error('Error fetching followers:', error);
            });
        console.log('requester id', requestId)
        console.log('all following', followingList)
    };


    /*
    1. check followers list - that means mutual friendship not establshed / has being cut 
    2. if not in this list then set (setSentrequest) to empty set



    */
    const fetchSentFriendRequests = () => {
        axiosInstance.get(`authors/${userId}/followers/sentFriendRequests/`)
            .then(response => {
                console.log('response of request i have ', response.data)
                const requests = new Set(response.data.map(req => extractUUIDFromURL(req.object.id)));
                console.log('requests', requests)
                setSentRequests(requests);

                // console.log('sent friend request', sentRequests)
            })
            .catch(error => console.error('Error fetching sent friend requests:', error));
    };


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
                setButtonState('Request Sent')
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

    const getdisabledState = (userUUID) => {
        if (!followingList.includes(userUUID)) {
            return false;
        } else if (sentRequests.has(userUUID)) {
            return true;
        }
    };


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
