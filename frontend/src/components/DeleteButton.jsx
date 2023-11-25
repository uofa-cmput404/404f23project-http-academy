import React from 'react';
import axiosInstance from '../axiosInstance';
import { useNavigate } from "react-router-dom";

export default function DeleteButton({ postId, onClose }) {
  // TODO: Add CSS 
  let navigate = useNavigate();
  const storedUser_val = JSON.parse(localStorage.getItem('user'));
  const storedUser = storedUser_val.user
  const userId = storedUser.id.split("/").pop()
  const handleDelete = () => {

    const url = "authors/" + userId + "/posts/" + postId + "/";
    axiosInstance.delete(url).then(response => {
      // console.log(response);
      navigate("/home");
    }).catch(error => {
      console.log(error);
    });
    onClose();
  };

  return (
    <div>
      <button onClick={handleDelete}>Delete</button>
    </div>
  );
}