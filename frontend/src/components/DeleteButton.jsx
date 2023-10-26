import React from 'react';
import axiosInstance from '../axiosInstance';
import { useNavigate } from "react-router-dom";

export default function DeleteButton({ id }) {
  let navigate = useNavigate();
  const handleDelete = () => {
    axiosInstance.delete(`posts/${id}`).then(response => {
      // console.log(response);
      navigate("/home");
    }).catch(error => {
      console.log(error);
    });
  };

  return (
    <div>
      <button onClick={handleDelete}>Delete</button>
    </div>
  );
}