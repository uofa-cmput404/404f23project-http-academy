import React, {useEffect, useState} from "react";
import "../css/Post.css"
import { Link } from 'react-router-dom'
import { useNavigate } from "react-router-dom";
import editIcon from '../assets/images/ellipsis.png'
import likeIcon from '../assets/images/heart.png'
import commentIcon from '../assets/images/chat.png'
import Modal from "../components/Modal";
import EditPost from "../components/EditPost"

export default function Post({ post, canEdit }) {

    const [openModal, setOpenModal] = useState(false);
    const [modalMode, setModalMode] = useState("");
    console.log('edit prop', canEdit)
    let navigate = useNavigate();
    

    const handleEdit = () => {
        // Your like functionality here
        console.log('Edit button clicked');
    };
    
  

    const handleLike = () => {
        // Your like functionality here
        console.log('Like button clicked');
    };
    
  

    const handleComment = () => {
        // Your like functionality here
        console.log('Comment button clicked');
    };
    
  

    // Overrides the anchor tag styling caused by the Link component
    const neutral = {
        color: 'black',
        textDecoration: 'none'
    }

      //if the post is made by the current logged in user then display edit button 
  //else dont 
  
  const storedUser = JSON.parse(localStorage.getItem('user'));
    
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

    return (
        <div className="card">
            <div className="Editpost">
                { canEdit ? (
                <button onClick={editPost} className="edit-button">
                <img src={editIcon} alt="Edit" />
                </button> ): " "}
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
            {storedUser.username} 
            </div>
           
            <div className="card-footer">
                <button onClick={handleLike} className="edit-button">
                    <img src={likeIcon} alt="Like" />
                </button>
                <button onClick={handleComment} className="edit-button">
                    <img src={commentIcon} alt="Like" />
                </button>
                
            </div>

            {openModal && <Modal isOpen={openModal} mode = {modalMode} post = {post} onClose={() => setOpenModal(false)} />}
          </div>

            {/* {canEdit ?  (
          <button onClick={editPost}>Edit</button> ): " "} */}
        </div>
    );
}