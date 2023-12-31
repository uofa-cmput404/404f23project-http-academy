// Import necessary functions and components
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import DeleteButton from "./DeleteButton";

// Define the EditPost component
export default function EditPost({ onClose, posts }) {
  // Define state variables
  const [post, setPost] = useState(null);
  const [image, setImage] = useState("");
  const [visibility, setVisibility] = useState("");
  const storedUser_val = JSON.parse(localStorage.getItem('user'));
  const storedUser = storedUser_val.user
  const userId = storedUser.id.split("/").pop()
  const navigate = useNavigate();
  console.log('postsss', posts)
  const postId = posts.post_id;


  const url = `authors/${userId}/posts/${postId}/`;

  useEffect(() => {
    axiosInstance
      .get(url)
      .then((retrievedPost) => {
        console.log("Post fetched for editing", retrievedPost);
        setPost(retrievedPost.data);
        setVisibility(retrievedPost.data.visibility);


        if (retrievedPost.data.image) {
          setImage(retrievedPost.data.image);



        }

      })
      .catch((error) => {
        console.log("Error fetching post for editing", error);
      });


  }, [postId, posts, url]);

  const editPost = (updatedTitle, updatedBody, updatedUrl, updatedImage) => {


    if (post.title !== updatedTitle) {
      post.title = updatedTitle;
    }
    if (post.content !== updatedBody) {
      post.content = updatedBody;
    }

    if (post.image !== updatedImage) {
      post.image = updatedImage;
    }

    if (post.visibility !== visibility) {
      post.visibility = visibility;
    }

    if (post.image_url !== updatedUrl) {
      post.image_url = updatedUrl;
    }
   

    const updatedPost = {
      title: post.title,
      content: post.content,
      image: post.image,
      visibility: visibility,
      image_url: post.image_url
    };

    console.log('this is sedning to backend', post);
    axiosInstance
      .patch(url, updatedPost)
      .then((response) => {
        console.log('server response', response);
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
            <button className={visibility === "PUBLIC" ? "selected" : ""} onClick={() => setVisibility("PUBLIC")}>Public</button>
            <button className={visibility === "FRIENDS_ONLY" ? "selected" : ""} onClick={() => setVisibility("FRIENDS_ONLY")}>Friends-Only</button>
            <button className={visibility === "PRIVATE" ? "selected" : ""} onClick={() => setVisibility("PRIVATE")}>Private</button>
            <button className={visibility === "UNLISTED" ? "selected" : ""} onClick={() => setVisibility("UNLISTED")}>Unlisted</button>

          </div>
          <h2>Title</h2>
          <input type="text" id="title" name="title" class="single-line-input" defaultValue={post.title} />
          <h2>Body</h2>
          <textarea id="body" name="body" rows="4" cols="50" defaultValue={post.content} class="single-line-input"></textarea>

          <h2>Image URL</h2>
				  <input type="text" id="image_url" name="image_url" defaultValue={post.image_url} class="single-line-input" maxLength={50} />
		

          <br />
          <div className="postfooter-container">
            <input type="file" accept="image/*" onChange={handleImageUpload} />
            <button
              onClick={() =>
                editPost(
                  document.getElementById("title").value,
                  document.getElementById("body").value,
                  document.getElementById("image_url").value,
                  image
                )
              }
            >
              Save Changes
            </button>

            <DeleteButton postId={postId} onClose={onClose} />
          </div>

          {/* <button onClick={onClose}>Back</button> */}
        </div>
        <div className="rightContainer">



          <h2>Preview</h2>
          <div className="preview-image" style={{
            backgroundImage: image ? `url(${image})` : '',
            backgroundSize: 'cover',
            backgroundPosition: 'center center'
          }}>
            {!image && <div className="no-image">No image uploaded</div>}
          </div>








        </div>
      </div>
    );
  }
}
