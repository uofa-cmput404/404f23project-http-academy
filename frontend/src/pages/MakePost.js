import React, { useState } from "react";
import "../css/MakePost.css";
import axiosInstance from "../axiosInstance";

export default function MakePost({ onClose }) {

	const [visibility, setVisibility] = useState("PUBLIC");
	const storedUser_val = JSON.parse(localStorage.getItem('user'));
	const storedUser = storedUser_val.user;
	const userId = storedUser.id.split("/").pop();
	const addPost = (title, body, image_url) => {
		// TODO: add POST to backend here
		if (title === "") {
			alert("Please add a title to your post ");
			return;
		}
		// console.log(title, body);
		// TODO: add author details, etc. here


		const url = "authors/" + userId + "/posts/";

		const postSent = {
			type: "post",
			author: userId,
			title: title,
			image: image ? image : null,
			content: body ? body : null,
			visibility: visibility,
			unlisted: false,
			image_url: image_url
		};

		console.log('post dataa', postSent);
		axiosInstance.post(url, postSent).then(response => {
			console.log('post created', response);
		}).catch(error => {
			console.log(error);
		});
		// navigate("/home");
		onClose(); //we close the model after we succesful make a post
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
				<div className="visibility-container">
					<h2 className="visibility">Visibility</h2>
					<div className="visibility-section">
						<button className={visibility === "PUBLIC" ? "selected" : ""} onClick={() => setVisibility("PUBLIC")}>Public</button>
						<button className={visibility === "FRIENDS_ONLY" ? "selected" : ""} onClick={() => setVisibility("FRIENDS_ONLY")}>Friends-Only</button>
						<button className={visibility === "PRIVATE" ? "selected" : ""} onClick={() => setVisibility("PRIVATE")}>Private</button>
						<button className={visibility === "UNLISTED" ? "selected" : ""} onClick={() => setVisibility("UNLISTED")}>Unlisted</button>
					</div>
				</div>
				<h2>Image URL</h2>
				<input type="text" id="image_url" name="image_url" class="single-line-input" maxLength={50} />
				{/* <h2>Title</h2>
				<input type="text" id="title" name="title" class="single-line-input" maxLength={80} /> */}
				<h2>Body</h2>
				<textarea id="body" name="body" rows="4" cols="50" class="single-line-input"></textarea>


				<br />
				<div className="postfooter-container">
					<input type="file" accept="image/*" onChange={handleImageUpload} />
					<button onClick={() => addPost(document.getElementById("title").value, document.getElementById("body").value, document.getElementById("image_url"))}>Post</button>
				</div>


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

