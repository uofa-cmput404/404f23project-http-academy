import React, { useState, useEffect } from "react";
import axiosInstance from "../axiosInstance";

export default function LikeButton({ id }) {
  const [likeCount, setLikeCount] = useState(0);
  // const storedUser = JSON.parse(localStorage.getItem('user'));

  // TODO: Move logic out
  useEffect(() => {
    axiosInstance.get(`posts/${id}/like/`).then(response => {
      // console.log(response);
      setLikeCount(response.data);
    }).catch(error => {
      console.log(error);
    });
  });

  const handleLike = () => {
    axiosInstance.post(`posts/${id}/like/`).then(response => {
      // console.log(response);
    }).catch(error => {
      console.log(error);
    });
    setLikeCount(likeCount + 1);
  };

  return (
    <div>
      <button onClick={handleLike}>Like</button>
      <span>{likeCount}</span>
    </div>
  );
}

//user can like post once

/*
1. get current user and post and if user alread yhas a liek on the post then show it
. if not then like should be 0, 

*/