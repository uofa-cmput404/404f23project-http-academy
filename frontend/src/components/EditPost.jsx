// Import necessary functions and components
import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import DeleteButton from "./DeleteButton";

// Define the EditPost component
export default function EditPost() {
  // Define state variables
  const [post, setPost] = useState(null);
  const [image, setImage] = useState("");
  const [imagePreview, setImagePreview] = useState(null);

  
  const navigate = useNavigate();
  const { id } = useParams();




  useEffect(() => {
    axiosInstance
      .get(`posts/${id}`)
      .then((retrievedPost) => {
        console.log("Post fetched for editing", retrievedPost);
        setPost(retrievedPost.data);
       
        // if (retrievedPost.contentType.startsWith('image/')) {
        //   setImagePreview(`data:${retrievedPost.contentType};base64,${retrievedPost.content}`);
        // }
        if (retrievedPost.data.image){
            setImage(retrievedPost.data.image)
            setImagePreview(retrievedPost.data.image)
            
        }
        
      })
      .catch((error) => {
        console.log("Error fetching post for editing", error);
      });
  }, [id]);

  const returnHome = () => {
    navigate("/home");
  };


//   const deletePost = () => {
//     const confirmDelete = window.confirm(
//       "Are you sure you want to delete this post?"
//     );
//     if (confirmDelete) {
//       postService
//         .remove(id)
//         .then(() => {
//           navigate("/home");
//         })
//         .catch((error) => {
//           console.log("Error deleting post", error);
//         });
//     }
//   };


  const editPost = (updatedTitle, updatedBody, updatedImage) => {
   
   
    if (post.title !== updatedTitle){
        post.title = updatedTitle; 
    }
    if (post.content !== updatedBody) {
        post.content = updatedBody; 
    }
   
    if (post.image !== updatedImage){
        post.image = updatedImage
    }
 
    const updatedPost = {
        title: post.title,
        content: post.content,
        image: post.image
    }

    
 
    console.log('this is sedning to backend', post)
    axiosInstance
      .patch(`posts/${id}`, updatedPost)
      .then((response) => {
        console.log('server response', response)
        navigate("/home");
        
      })
      
      .catch((error) => {
        console.log("Error updating post", error);
      });
  };

  // Handle the image upload
  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();

        reader.onload = (e) => {
            console.log(e.target.result);
            setImage(e.target.result);
            setImagePreview(e.target.result)
        };

        reader.readAsDataURL(file);
    }
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
          defaultValue={post.content}
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
        <DeleteButton id = {id}/>
        <button onClick={returnHome}>Back</button>
      </div>
    );
  }
}
