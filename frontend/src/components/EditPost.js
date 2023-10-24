// Import necessary functions and components
import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import postService from "../services/posts";

// Define the EditPost component
export default function EditPost() {
  // Define state variables
  const [post, setPost] = useState(null);
  const [image, setImage] = useState("");
  const [imagePreview, setImagePreview] = useState(null);

 
  const navigate = useNavigate();
  const { id } = useParams();

  useEffect(() => {
    postService
      .get(id)
      .then((retrievedPost) => {
        console.log("Post fetched for editing", retrievedPost);
        setPost(retrievedPost);
        if (retrievedPost.contentType.startsWith('image/')) {
          setImagePreview(`data:${retrievedPost.contentType};base64,${retrievedPost.content}`);
        }
        
        
      })
      .catch((error) => {
        console.log("Error fetching post for editing", error);
      });
  }, [id]);

  const returnHome = () => {
    navigate("/home");
  };


  const deletePost = () => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this post?"
    );
    if (confirmDelete) {
      postService
        .remove(id)
        .then(() => {
          navigate("/home");
        })
        .catch((error) => {
          console.log("Error deleting post", error);
        });
    }
  };


  const editPost = (updatedTitle, updatedBody, updatedImage) => {

    if (updatedTitle === "" || updatedBody === "") {
      alert("Please fill out all fields");
      return;
    }


   
    const updatedPost = {
      ...post,
      title: updatedTitle,
      description: updatedBody,
      content: updatedImage || post.content,
    };
    postService
      .update(id, updatedPost)
      .then((newPost) => {
        navigate("/home");
      })
      .catch((error) => {
        console.log("Error updating post", error);
      });
  };

  // Handle the image upload
  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (!file) {
      return; // No file was selected, so don't change the image state
    }
    const reader = new FileReader();
    reader.onloadend = () => {
      const base64content = reader.result.split(',')[1];
      setImage(base64content);
      setImagePreview(reader.result);
    };
    reader.onerror = (error) => {
      console.log('Error reading file:', error);
    };
    reader.readAsDataURL(file);
  };
  


  if (post === null) {
    return <div>Loading...</div>;
  } else {
    return (
      <div>
        <h1>Edit Post</h1>
        <h2>Title</h2>
        <input
          type="text"
          id="title"
          name="title"
          defaultValue={post.title}
        />
        <h2>Body</h2>
        <textarea
          id="body"
          name="body"
          rows="4"
          cols="50"
          defaultValue={post.description}
        ></textarea>
        <h2>Image</h2>
        {imagePreview && <img src={imagePreview} alt="Post" style={{ maxWidth: '100px', maxHeight: '100px' }} />} 
        <input type="file" onChange={handleImageUpload} />
        <br />
        <button
          onClick={() =>
            editPost(
              document.getElementById("title").value,
              document.getElementById("body").value,
              image
            )
          }
        >
          Save Changes
        </button>
        <button onClick={deletePost}>Delete Post</button>
        <button onClick={returnHome}>Back</button>
      </div>
    );
  }
}
