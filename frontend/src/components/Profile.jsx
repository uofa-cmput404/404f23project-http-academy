import { Avatar, Button, Dialog, DialogActions, DialogContent, DialogTitle, Divider, IconButton, List, ListItem, ListItemText, Tab, Tabs } from "@mui/material";
import React, { useState, useEffect } from "react";
// import Post from "./Post";
// import "./Profile.css"
import axiosInstance from "../axiosInstance";
import axios from "axios";
import { red } from "@mui/material/colors";
import AddIcon from '@mui/icons-material/Add';
// import CreateNewPost from "./CreateNewPost";
import FriendItem from "./FriendItem";

const Profile = () => {

  const [openCreateDialog, setOpenCreateDialog] = useState(false);
  const [allPosts, setAllPosts] = useState([]);
  const [allFollowers, setAllFollowers] = useState([]);
  const [tabIndex, setTabIndex] = useState(0);
  const [allFriends, setAllFriends] = useState([]);
  const authorObject = JSON.parse(localStorage.getItem("user"));
  const author = JSON.parse(localStorage.getItem('user'));
  const authorId = author.user.id
  console.log('my details', authorId)


  useEffect(() => {
    getPosts();
    getFollowers();
  }, [])
  const getFollowers = () => {
    const url = "authors/" + authorId + "/followers/"

    axiosInstance.get(url)
      .then((response) => {
        setAllFollowers(response.data.items);
        console.log("AllFollowers:", allFollowers);

      });
  }

  const getFriends = async (followers) => {
    console.log("GetFriends");
    console.log("All followers length,", followers.length);

    // to check if a follower is a friend
    const checkIfFriend = async (follower) => {
      const followerID = follower.id.split("/").pop();
      const url = `authors/${followerID}/followers/${authorId}`;
      try {
        const response = await axiosInstance.get(url);
        return !response.data.detail;
      } catch (error) {
        console.error('Error checking friend status:', error);
        return false;
      }
    };

    try {
      // Use Promise.all to wait for all friend checks to complete
      const friends = await Promise.all(followers.map(async (follower) => {
        const isFriend = await checkIfFriend(follower);
        return isFriend ? follower : null;
      }));

      // Filter out null values and set the friends
      const filteredFriends = friends.filter(friend => friend !== null);
      setAllFriends(filteredFriends);
      console.log("All Friends:", filteredFriends);
    } catch (error) {
      console.error('Error getting friends:', error);
    }
  };


  const getPosts = () => {

    const userid = authorId.split("/").pop();
    const url = "authors/" + userid + "/posts/"
    console.log('url sent', url)
    axiosInstance.get(url).then((response) => {
      console.log('got back', response.data.items)
      setAllPosts(response.data.items);
    });

  }


  function checkNoFollowers() {
    if (allFollowers.length === 0) {
      return true
    }
    return false;
  }

  function checkNoFriends() {
    if (allFriends.length === 0) {
      return true
    }
    return false
  }


}

export default Profile;