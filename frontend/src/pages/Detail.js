import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import DetailedPost from "../components/DetailedPost";
import axiosInstance from "../axiosInstance";

export default function Detail() {
  const { id } = useParams();

  const defaultPost = { title: "Test", body: "Body" };
  const [post, setPost] = useState(defaultPost);

  useEffect(() => {
    axiosInstance.get(`posts/${id}`).then(response => {
      console.log(response.data);
      setPost(response.data);
    }).catch(error => {
      console.log(error);
    });
  }, [id]);

  return (
    <div>
      {/* <h1>Detailed Post for Post: {id}</h1> */}
      {/* Specifically passing id in because grabbing post.id in DetailedPost causes problems */}
      <DetailedPost post={post} id={id} image={post.image} />
    </div>
  );
}