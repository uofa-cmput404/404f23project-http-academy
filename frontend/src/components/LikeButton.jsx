import React, { useState, useEffect } from "react";
import axiosInstance from "../axiosInstance";

export default function LikeButton({ id }) {
  const [likes, setLikes] = useState({});
  const [likeCount, setLikeCount] = useState(0)
  const storedUser = JSON.parse(localStorage.getItem('user'));
  // const storedUser = JSON.parse(localStorage.getItem('user'));

  // TODO: Move logic out
  // Use useEffect with an empty dependency array to fetch likes only once when the component mounts
  useEffect(() => {
    axiosInstance.get(`posts/${id}/like/`).then(response => {
      console.log("response.data: ", response.data);
      setLikes(response.data);  // Update likes array
      setLikeCount(response.data.length);  // Update likeCount
    }).catch(error => {
      console.log(error);
    });
  }, []);  // Dependency array is empty, so this effect runs only once when the component mounts

  /*
  const handleLike = () => {
    axiosInstance.post(`posts/${id}/like/`).then(response => {
      // console.log(response);
    }).catch(error => {
      console.log(error);
    });
    setLikeCount(likeCount + 1);
  };
*/
  const addPostLike = () => {


    // Check if the user has already liked the post
    if (likes.some(like => like.author === storedUser.id)) {
      // User has already liked the post, handle accordingly
      console.log("User has already liked the post");
      return;
    }

    axiosInstance.post(`posts/${id}/like/`, {
      postId: id,
      author: storedUser.id,

    }).then(response => {
      console.log(response);
      // after creating a new like, how can I update the number of likes being displayed?
      setLikes([...likes, { id: response.data.id, author: storedUser.id, postId: id }]);
      setLikeCount(prevLikeCount => prevLikeCount + 1);
      console.log("like count: " + likeCount)
    }).catch(error => {
      console.log(error);
    });
  };


  return (
    <div>
      <button onClick={addPostLike}>Like</button>
      <span>{likeCount}</span>
    </div>
  );
}

//user can like post once

/*
1. get current user and post and if user alread yhas a liek on the post then show it
. if not then like should be 0, 

*/