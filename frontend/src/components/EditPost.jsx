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
  const [contentType, setContentType] = useState("");

  const navigate = useNavigate();
  const id = posts;

  console.log('modal post', posts);

  useEffect(() => {
    axiosInstance
      .get(`posts/${id}`)
      .then((retrievedPost) => {
        console.log("Post fetched for editing", retrievedPost);
        setPost(retrievedPost.data);
        setVisibility(retrievedPost.data.visibility);
        setContentType(retrievedPost.data.contentType);
        console.log("HELLO!!!!!", contentType);
        console.log("RETRIEVED!!!!", retrievedPost.data.contentType);

        if (retrievedPost.data.image) {
          setImage(retrievedPost.data.image);
        }

      })
      .catch((error) => {
        console.log("Error fetching post for editing", error);
      });

  }, [id]);

  const editPost = (updatedTitle, updatedBody, updatedImage) => {

    console.log("??????", contentType, post.contentType);
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

    if (post.contentType !== contentType) {
      console.log("Inside if statement", contentType, post.contentType);
      post.contentType = contentType;
    }

    const updatedPost = {
      title: post.title,
      content: post.content,
      image: post.image,
      contentType: contentType,
      visibility: visibility
    };

    console.log('this is sedning to backend', post);
    axiosInstance
      .patch(`posts/${id}`, updatedPost)
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

  const handleContentChange = (event) => {
    setContentType(event.target.value);
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
          <h2>{contentType}</h2>
          <div>
            <h2 className="contentType">Content Type</h2>
            <select
              onChange={handleContentChange}
              className="text-select"
              value={contentType}
            >
              <option value="plainText">Plain Text</option>
              <option value="markdown">Markdown</option>

            </select>
          </div>
          <h2>Title</h2>
          <input type="text" id="title" name="title" className="single-line-input" defaultValue={post.title} />
          <h2>Body</h2>
          <textarea id="body" name="body" rows="4" cols="50" defaultValue={post.content} className="single-line-input"></textarea>


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

            <DeleteButton id={id} onClose={onClose} />
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
