import React, { useState } from "react";
import { useParams } from "react-router-dom";
import axiosInstance from "../axiosInstance";

export default function Image() {
  const { id } = useParams();
  const [image, setImage] = useState("");

  axiosInstance.get(`posts/${id}/image`).then(response => {
    // console.log(response.data);
    setImage(response.data);
  }).catch(error => {
    console.log(error);
  }, [id]);

  return (
    <div>
      {image ? <img src={`${image}`} alt="Base64" /> : <h1>There is no image associated with this post.</h1>}
    </div>
  );
}