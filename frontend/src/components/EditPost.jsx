// Import necessary functions and components
import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import DeleteButton from "./DeleteButton";

// Define the EditPost component
export default function EditPost({onClose, posts}) {
  // Define state variables
  const [post, setPost] = useState(null);
  const [image, setImage] = useState("");
  const [imagePreview, setImagePreview] = useState(null);
  const [visibility, setVisibility] = useState("PUBLIC")
  
  const navigate = useNavigate();
  const  id  = posts;

  console.log('modal post', posts)




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
      onClose();
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
      <div className="Create-postContainer">
			<div className="leftContainer">
				<div className="post-header">
				<h1>Edit a <br></br> Post.</h1>
				<button className="close-button" onClick={onClose} aria-label="Close">X</button>
					</div>
				
				<h2 className="visibility">Visibility</h2>
				<div className="visibility-section">
					<button onClick={() => setVisibility("PUBLIC")}>Public</button>
					<button onClick={() => setVisibility("FRIENDS_ONLY")}>Friends-Only</button>
					<button onClick={() => setVisibility("PRIVATE")}>Private</button>
					<button onClick={() => setVisibility("UNLISTED")}>Unlisted</button>
				</div>
				<h2>Title</h2>
					<input type="text" id="title" name="title" class="single-line-input" defaultValue={post.title}/>
					<h2>Body</h2>
					<textarea id="body" name="body" rows="4" cols="50" defaultValue={post.content} class="single-line-input"></textarea>
					

				<br />
				<div className="postfooter-container">
				<input type="file" accept="image/*" onChange={handleImageUpload} />
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

        <DeleteButton id = {id} onClose = {onClose} />
				</div>
				
				{/* <button onClick={onClose}>Back</button> */}
			</div>
			<div className="rightContainer">
				
      <h2>Preview</h2>
<div className="preview-image" style={{ 
  backgroundImage: imagePreview ? `url(${imagePreview})` : (image ? `url(${image})` : ''),
  backgroundSize: 'cover', 
  backgroundPosition: 'center center',
  display: imagePreview || image ? 'block' : 'none' // Hide the div if no image is available
}}>
  {(!image && !imagePreview) && <div className="no-image">No image uploaded</div>}
</div>




				
			</div>
		</div>
    );
  }
}


{/* <button
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

<DeleteButton id = {id}/> */}