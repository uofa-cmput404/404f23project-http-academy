import React, { useEffect, useState } from 'react';
import axiosInstance from '../axiosInstance';
import { List, ListItem, ListItemText } from '@mui/material';

export default function SharePost({ posts, users }) {

    const [userToSend, setUserToSend] = useState("")
    const [post, setPost] = useState([])
    useEffect(()=>{
        setPost(posts)
    })

    const selectUser = (userID) =>{
        if (userToSend === ""){
            setUserToSend(userID)
        }
        else{
            setUserToSend("")
        }
    }
    const sharePostWithUser = (userToSend) => {
        
        selectUser(userToSend)
        console.log("sharing post to:", userToSend);
        
        // Extract just the ID from the authorToSend URL
        const authorIdString = new URL(userToSend).pathname.split('/').pop();
        const authorId = parseInt(authorIdString, 10);
        console.log(authorId, typeof(authorId))
        // I Construct URL using the extracted author ID
        const postUrl = `authors/${authorId}/inbox/`;
    
        // delete post.authorDetails;
        console.log("Sending post to URL:", postUrl);
        console.log("this is post i sedning:", post);
        
        
        axiosInstance.post(postUrl, post)
            .then((response) => {
                console.log("post shared", response);
                setUserToSend("");
               
            })
            .catch(error => {
                console.error('Error sharing post', error);
            });
    };
    
  return (
    <List>
      {users.map((user) => (
        <ListItem 
          button 
          key={user.id} 
          onClick={() => sharePostWithUser(user.id)}
        >
          <ListItemText primary={user.displayName} />
        </ListItem>
      ))}
    </List>
  );
}
