
import axiosInstance from "../axiosInstance";
import React, { useState } from "react";
import "../css/Post.css";
import { Link } from 'react-router-dom';
import editIcon from '../assets/images/ellipsis.png';
// import likeIcon from '../assets/images/heart.png';
import commentIcon from '../assets/images/chat.png';
import Modal from "../components/Modal";
import shareIcon from '../assets/images/share.png';
import FavoriteBorderOutlinedIcon from '@mui/icons-material/FavoriteBorderOutlined';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import ShareOutlinedIcon from '@mui/icons-material/ShareOutlined';
import ModeOutlinedIcon from '@mui/icons-material/ModeOutlined';

export default function Post({ post, canEdit }) {

    const [openModal, setOpenModal] = useState(false);
    const [modalMode, setModalMode] = useState("");
    const [liked, setLiked] = useState(false)
    console.log('edit prop', canEdit);



    // const handleEdit = () => {
    //     // Your like functionality here
    //     console.log('Edit button clicked');
    // };


    const handleLike = () => {
        // Your like functionality here
        console.log('Like button clicked');
        setLiked(!liked)
    };

    const handleComment = () => {
        // Your like functionality here
        console.log('Comment button clicked');
    };

    // Overrides the anchor tag styling caused by the Link component
    const neutral = {
        color: 'black',
        textDecoration: 'none'
    };

    //if the post is made by the current logged in user then display edit button 
    //else dont 

    // const storedUser = JSON.parse(localStorage.getItem('user'));

    //   console.log(storedUser)
    // const editPost = () => {

    //     console.log('can edit', canEdit)
    //     navigate(`/post/edit/${post.id}`);
    // }




    const editPost = () => {
        // Open the modal and set it to show the EditPost component
        setModalMode('edit');
        setOpenModal(true);
    };


      //if the post is made by the current logged in user then display edit button 
  //else dont 
  


    const handleShare = () => {
        console.log('Share icon clicked', `localhost`);
      
    
        axiosInstance.get(`posts/shareable_link/${post.id}`).then(response => {
            
            console.log('url copied to user', response.data.url);
            let rewritternUrl = response.data.url.replace('localhost:8000/posts', 'localhost:3000/post')
            console.log('heeee', rewritternUrl)
            navigator.clipboard.writeText(response.data.url).then(() => {
                console.log('Link copied to clipboard');
            }).catch(err => {
                console.error('Could not copy text: ', err);
            });
            
        }).catch(error => {
            console.log(error);
        });
    }
    

    return (
        <div className="card">
            <div className="edit-container">
                
            <button onClick={editPost} className={`edit-button ${canEdit ? "" : "invisible"}`}>
                <img src={editIcon} alt="Edit" />
            </button>
            </div>
            

            <Link to={`/post/${post.id}`} style={neutral}>
            <div className="card-body">
                <h2 className="card-title">{post.title}</h2>
                {/* <p className="card-text">{post.content}</p> */}
            </div>
           <h3>{canEdit}</h3>
          </Link>
          <div className="footer-container">
            <div className="userNamePost">
                {/* need to include the actual user name of the user who made the post
                the below is wrong - this is the current logged in user 
                */}
            {/* {storedUser.username}  */} 
            </div>
           
            <div className="card-footer">
            {liked ? (
                <FavoriteIcon onClick={handleLike} style={{ fontSize: '40px', color: 'red', cursor: 'pointer', marginRight: '10px' }} />
            ) : (
                <FavoriteBorderOutlinedIcon onClick={handleLike} style={{ fontSize: '40px', cursor: 'pointer', marginRight: '10px' }} />
            )}

            <ChatBubbleOutlineIcon onClick={handleComment} style={{ fontSize: '40px', cursor: 'pointer' , marginRight: '10px'}} />
            <ShareOutlinedIcon onClick={handleShare} style={{ fontSize: '40px', cursor: 'pointer' }} />
                
                
            </div>

            {openModal && <Modal isOpen={openModal} mode = {modalMode} post = {post} onClose={() => setOpenModal(false)} />}
          </div>

            {/* {canEdit ?  (
          <button onClick={editPost}>Edit</button> ): " "} */}
        </div>
    );
}
