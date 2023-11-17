import React, { useEffect, useState } from "react";
import "../css/Profile.css";
import axiosInstance from "../axiosInstance";
import { useLocation } from "react-router-dom";

const Profile = () => {
  const [username, setUsername] = useState("");
  const [editMode, setEditMode] = useState(false);
  const [error, setError] = useState("");
  const [hasSentRequest, setHasSentRequest] = useState(false);
  const location = useLocation();
  const [author, setAuthor] = useState(null); 
  const currentUserId = JSON.parse(localStorage.getItem('user')).id.toString();
  const userObject = JSON.parse(localStorage.getItem('user'));

  useEffect(() => {
    if (location.state && location.state.author) {
      setUsername(location.state.author.displayName);
      setAuthor(location.state.author);
      checkFriendRequest(location.state.author.numericId);
    }
  }, [location.state]); 

  // const checkFriendRequest = async (authorId) => {
  //   try {
  //     const response = await axiosInstance.get(`authors/${currentUserId}/followers/friendrequests/`);
  //     const requestExists = response.data.items.some(request => 
  //       request.actor.user_id === currentUserId && request.object.user_id === authorId
  //     );
  //     setHasSentRequest(requestExists);
  //   } catch (error) {
  //     console.error('Error checking friend request', error);
  //   }
  // };


  const checkFriendRequest = async () => {
    try {
     
      const response = await axiosInstance.get(`authors/${currentUserId}/followers/sentFriendRequests/`);
      const targetAuthorId = parseInt(location.state.author.id.split("/").pop(), 10);
  
      const requestExists = response.data.some(request => 
        request.object.user_id === targetAuthorId
      );
      setHasSentRequest(requestExists);
    } catch (error) {
      console.error('Error checking sent friend requests', error);
    }
  };

  
  const followUser = async () => {
    if (!author || hasSentRequest) return;

    const type = "follow";
    const authorId = parseInt(location.state.author.id.split("/").pop(), 10);
    // console.log('am hete', location.state.author)
    const postData = {
      type: "Follow",
      summary: userObject.username + " sent you a friend request.",
      object: {
        type: type,
        id: authorId,
        host: location.state.author.host,
        displayName: username,
        url: location.state.author.url,
        github: location.state.github,
        profileImage: location.state.profileImage
      },
      actor: userObject,
    };

    const requestUrl = `authors/${authorId}/inbox/`;
    try {
      const response = await axiosInstance.post(requestUrl, postData);
      console.log('Friend request was sent', response.data);
      setHasSentRequest(true); // Update state to reflect the new friend request
    } catch (error) {
      console.log(error);
    }
  };


  return (
    <div>
      {username}
      {author && currentUserId.toString() !== author.numericId && (
        <button onClick={followUser} disabled={hasSentRequest}>
          {hasSentRequest ? 'Request Sent' : 'Follow'}
        </button>
      )}
    </div>
  );
  
};

export default Profile;
