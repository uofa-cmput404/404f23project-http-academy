import React, { useEffect, useState } from 'react';
import axiosInstance from '../axiosInstance';
import { Button, List, ListItem, ListItemText } from '@mui/material';
import '../css/SharePost.css';
import { extractUUIDFromURL } from '../utilities/extractUIID'
export default function SharePost({ posts, users }) {
  const [selectedUserId, setSelectedUserId] = useState(null);
  const [post, setPost] = useState([]);

  useEffect(() => {
    console.log('posts gotten from modal', posts);
    console.log('users gotten from modal', users);
    setPost(posts);
  }, [posts, users]);

  const selectUser = (userID) => {
    setSelectedUserId(userID === selectedUserId ? null : userID);
  };

  const sharePostWithUser = () => {
    if (!selectedUserId) {
      console.log("No user selected");
      return;
    }

    console.log("Sharing post with:", selectedUserId);


    // // Extract just the ID from the authorToSend URL
    const authorSendingPostTo = extractUUIDFromURL(selectedUserId);
    console.log('send to author inbx', authorSendingPostTo)
    // const authorId = parseInt(authorIdString, 10);
    // console.log(authorId, typeof (authorId))
    // // I Construct URL using the extracted author ID
    const postUrl = "authors/" + authorSendingPostTo + "/inbox/"

    // // delete post.authorDetails;
    // console.log("Sending post to URL:", postUrl);
    // console.log("this is post i sedning:", post);


    axiosInstance.post(postUrl, post)
      .then((response) => {
        console.log("post shared", response);


      })
      .catch(error => {
        console.error('Error sharing post', error);
      });
    setSelectedUserId(null);
  };

  return (
    <div className='outer-container'>
      <div className='full-contain'>
        <div>
          <h1>
            Share a <br></br> Post.
          </h1>
        </div>
        <div>
          <h4>Find your favorite person to share the moment!</h4>
        </div>
      </div>

      <div className='list-flex'>
        <List>
          {users.map((user) => (
            <ListItem
              button
              key={user.id}
              selected={user.id === selectedUserId}
              onClick={() => selectUser(user.id)}
            >
              <ListItemText primary={user.displayName} />
            </ListItem>
          ))}
        </List>
      </div>

      <div>
        <Button
          onClick={sharePostWithUser}
          style={{
            color: 'white', backgroundColor: 'black',
            width: '150px', height: '39px',
            position: 'absolute', bottom: '20px', right: '20px'
          }}
        >
          Share
        </Button>
      </div>
    </div>
  );
}

