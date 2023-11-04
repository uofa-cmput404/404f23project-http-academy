import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../css/MakePost.css";
import axiosInstance from "../axiosInstance";

export default function MakePost({onClose}) {

	let navigate = useNavigate();
	const [visibility, setVisibility] = useState("PUBLIC")
	const storedUser = JSON.parse(localStorage.getItem('user'));

	
	const addPost = (title, body) => {
		// TODO: add POST to backend here
		if (title === "") {
			alert("Please add a title to your post ");
			return;
		}
		// console.log(title, body);
		// TODO: add author details, etc. here
		axiosInstance.post('posts/', {
			author: storedUser.id,
			title: title,
			image: image ? image : null,
			content: body ? body : null,
			visibility: "PUBLIC",
			unlisted: false,
		}).then(response => {
			console.log('post created', response);
		}).catch(error => {
			console.log(error);
		});
		// navigate("/home");
		onClose(); //we close the model after we succesful make a post
	};

	const returnHome = () => {
		navigate("/home");
	};

	// Image handling
	const [image, setImage] = useState('');

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

	return (
		<div className="Create-postContainer">
			<div className="leftContainer">
				<div className="post-header">
				<h1>Create a <br></br> Post.</h1>
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
					<input type="text" id="title" name="title" class="single-line-input" />
					<h2>Body</h2>
					<textarea id="body" name="body" rows="4" cols="50" class="single-line-input"></textarea>
					

				<br />
				<div className="postfooter-container">
				<input type="file" accept="image/*" onChange={handleImageUpload} />
				<button onClick={() => addPost(document.getElementById("title").value, document.getElementById("body").value)}>Post</button>
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


// MakePost.jsx
// import React, { useState } from "react";
// import "../css/MakePost.css"; 
// import axiosInstance from "../axiosInstance";

// export default function MakePost({ onClose }) {
//   const [visibility, setVisibility] = useState("PUBLIC");
//   const [title, setTitle] = useState("");
//   const [body, setBody] = useState("");
//   const [image, setImage] = useState("");

//   const storedUser = JSON.parse(localStorage.getItem('user'));

//   const handleImageUpload = (event) => {
// 	const file = event.target.files[0];
// 	if (file) {
// 		const reader = new FileReader();

// 		reader.onload = (e) => {
// 			console.log(e.target.result);
// 			setImage(e.target.result);
// 		};

// 		reader.readAsDataURL(file);
// 	}
// };

// 	const addPost = (title, body) => {
// 		// TODO: add POST to backend here
// 		if (title === "") {
// 			alert("Please add a title to your post ");
// 			return;
// 		}
// 		// console.log(title, body);
// 		// TODO: add author details, etc. here
// 		axiosInstance.post('posts/', {
// 			author: storedUser.id,
// 			title: title,
// 			image: image ? image : null,
// 			content: body ? body : null,
// 			visibility: "PUBLIC",
// 			unlisted: false,
// 		}).then(response => {
// 			console.log('post created', response);
// 		}).catch(error => {
// 			console.log(error);
// 		});
// 		// navigate("/home");
// 		onClose(); //we close the model after we succesful make a post
// 	};
//   return (
//     <div className="create-post-container">
//       <div className="create-post-header">
//         <h1>Create a Post.</h1>
//         <button onClick={onClose} className="close-button">X</button>
//       </div>

//       <div className="visibility-section">
//         <button onClick={() => setVisibility("PUBLIC")}>Public</button>
//         <button onClick={() => setVisibility("FRIENDS_ONLY")}>Friends-Only</button>
//         <button onClick={() => setVisibility("PRIVATE")}>Private</button>
//         <button onClick={() => setVisibility("UNLISTED")}>Unlisted</button>
//       </div>

//       <input
//         type="text"
//         placeholder="Title"
//         value={title}
//         onChange={(e) => setTitle(e.target.value)}
//         className="title-input"
//       />

//       <textarea
//         placeholder="Craft your post"
//         value={body}
//         onChange={(e) => setBody(e.target.value)}
//         className="body-textarea"
//       ></textarea>

//       <input type="file" accept="image/*" onChange={handleImageUpload} />
//       {image && <img src={image} alt="Preview" className="image-preview" />}

//       <div className="post-actions">
//         <button onClick={() => addPost(document.getElementById("title").value, document.getElementById("body").value)} className="post-button">Post</button>
//       </div>
//     </div>
//   );
// }
