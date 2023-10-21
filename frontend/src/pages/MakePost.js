import React from "react";
import { useNavigate } from "react-router-dom";
import "../css/MakePost.css"

export default function MakePost() {

	let navigate = useNavigate();
	const addPost = (title, body) => {
		// TODO: add POST to backend here
		if (title === "" || body === "") {
			alert("Please fill out all fields");
			return;
		}
		console.log(title, body);
		navigate("/home");
	}

	const returnHome = () => {
		navigate("/home");
	}

	return (
		<div>
			<h1>Create a New Post</h1>
			<h2>Title</h2>
			<input type="text" id="title" name="title" />
			<h2>Body</h2>
			<textarea id="body" name="body" rows="4" cols="50"></textarea>
			<br />
			<button onClick={() => addPost(document.getElementById("title").value, document.getElementById("body").value)}>Add Post</button>
			<button onClick={() => returnHome()}>Back</button>
		</div>
	);
}