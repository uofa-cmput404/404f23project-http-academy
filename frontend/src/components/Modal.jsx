// Modal.jsx
import React from "react";
import "../css/Modal.css";
import MakePost from "../pages/MakePost";
import EditPost from "../components/EditPost";
import SharePost from '../components/SharePost'
import CommentPost from '../components/CommentPost'
const Modal = ({ isOpen, onClose, mode, post, users }) => {

  const getContent = () => {
    switch (mode) {
      case "make":
        return <MakePost onClose={onClose} />;
      case "edit":
        // console.log('post in modal', post)
        console.log('post in modal for editing', post)
        return <EditPost onClose={onClose} posts={post} />;

      case "Share":

        return <SharePost onClose={onClose} posts={post} users={users} />

      case "comment":

        return <CommentPost onClose={onClose} posts={post} users={users} />
      default:
        return null;
    }
  };

  return (
    isOpen && (
      <div className="modalOverlay" onClick={onClose}>
        <div className="modalContainer" onClick={(e) => e.stopPropagation()}>
          <div className="modalContent">
            {getContent()}
          </div>
        </div>
      </div>
    )
  );
};


export default Modal;
