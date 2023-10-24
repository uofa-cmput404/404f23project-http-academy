import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../css/MakePost.css";
import getCurrentDateTime from "../utils/datetime";
import postService from "../services/posts";
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import FormControl from '@mui/material/FormControl';

export default function MakePost() {
    const [post, setPost] = useState([]);
    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");
    const [contentType, setContentType] = useState("text/plain");
    const [visibility, setVisibility] = useState("Public");
	const [imagePreview, setImagePreview] = useState(null)
	const [image, setImage] = useState("");
	const [description, setDescription] = useState("");
	


    let navigate = useNavigate();

    const addPost = () => {
        if (title === "" || description === "") {
            alert("Please fill out all fields");
            return;
        }
        createPost(title, content, contentType, visibility, description);
        navigate("/home");
    };

    const generateID = () => {
        return '_' + Math.random().toString(36).substring(2, 9);
    };

    const createPost = (title, content, contentType, visibility, description) => {
		const postObject = {
			id: generateID(),
			type: "post",
			title: title,
			contentType: contentType,
			description: description,
			content: contentType.startsWith('image/') ? image : content,
			author: null,
			date: getCurrentDateTime(),
			likes: null,
			comments: [],
			visibility: visibility,
		};

		postService.create(postObject)
			.then(postCreated => {
			setPost(post.concat(postCreated));
			});
	};

    
    const TitleChange = (e) => {
        setTitle(e.target.value);
    };

	const DescriptionChange = (event) => {
		setDescription(event.target.value);
	  };
	

    // const handleContentChange = (event) => {
    // setContent(event.target.value);
	// };


	const handleImageChange = (event) => {
		const file = event.target.files[0];
		const reader = new FileReader();
		reader.onloadend = () => {
		  const result = reader.result;
		  if (result) {
			setImage(result.split(',')[1]); // remove the data url part
			setImagePreview(result); // set the image preview
		  } else {
			console.error("Failed to read the file.");
		  }
		};
		reader.onerror = (error) => {
		  console.error("Error reading file:", error);
		};
		reader.readAsDataURL(file);
	  };
	  


	const hiddenFileInput = React.useRef(null);
  
	const handleFileClick = event => {
		hiddenFileInput.current.click();
	};  


    const handleContentTypeChange = (event) => {
        setContentType(event.target.value);
    };

    const handleVisibilityChange = (event) => {
        setVisibility(event.target.value);
    };

    const returnHome = () => {
        navigate("/home");
    };

    return (
        <div>
            <h1>Create a New Post</h1>
            <h2>Title</h2>
            <input type="text" id="title" name="title" value={title} onChange={TitleChange} />
            <h2>Description</h2>
				<textarea id="description" name="description" rows="4" cols="50" value={description} onChange={DescriptionChange}></textarea>
				<div className="formElement">
          {/* If input type is image, show upload image button*/}
          {contentType === "image/png;base64" || contentType === "image/jpeg;base64" || contentType === "application/base64" ?
            <div className="UploadImage">
              <button variant="contained" component="label" onClick={handleFileClick}>
                Upload Image
                <input type="file" ref={hiddenFileInput} onChange={handleImageChange} hidden/>
              </button>
			  {imagePreview && <img src={imagePreview} alt="Post" style={{ maxWidth: '100px', maxHeight: '100px' }} />} 
            </div>
            : ""
          }

		
        </div>

            <br />
            <FormControl>
                <Select
                    value={contentType}
                    onChange={handleContentTypeChange}
                >
                    <MenuItem value={"text/plain"}>text/plain</MenuItem>
                    <MenuItem value={"application/base64"}>application/base64</MenuItem>
                    <MenuItem value={"image/png;base64"}>image/png;base64</MenuItem>
                    <MenuItem value={"image/jpeg;base64"}>image/jpeg;base64</MenuItem>
                </Select>
            </FormControl>
            <FormControl>
                <Select
                    value={visibility}
                    onChange={handleVisibilityChange}
                >
                    <MenuItem value={"Public"}>Public</MenuItem>
                    <MenuItem value={"Friends Only"}>Friends Only</MenuItem>
                    <MenuItem value={"Private"}>Private</MenuItem>
                    <MenuItem value={"Unlisted"}>Unlisted</MenuItem>
                </Select>
            </FormControl>
            <button onClick={() => addPost()}>Add Post</button>
            <button onClick={() => returnHome()}>Back</button>
        </div>
    );
}
