import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import axiosInstance from "../axiosInstance";
import "../css/Post.css";
import editIcon from '../assets/images/ellipsis.png';
import Modal from "../components/Modal";
import FavoriteBorderOutlinedIcon from '@mui/icons-material/FavoriteBorderOutlined';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import ShareOutlinedIcon from '@mui/icons-material/ShareOutlined';

export default function Post({ post, canEdit, authorDetails }) {
    const [openModal, setOpenModal] = useState(false);
    const [modalMode, setModalMode] = useState("");
    const [liked, setLiked] = useState(false);
    const [likesCount, setLikesCount] = useState(0);
    const [allusers, setAllUsers] = useState([]);
    // const [likeCount, setLikeCount] = useState(0)
    const loggedINUser = JSON.parse(localStorage.getItem('user'));
    const storedUser = loggedINUser?.user;
    const userId = storedUser?.id.split("/").pop();

    useEffect(() => {
        if (authorDetails) {
            console.log('Author Details:', authorDetails);
            fetchLikes();
            getAllUsers();

        }
    }, [authorDetails]);

    /*
        dprecated for now
    */
    // const goToAuthorProfile = () => {
    //     if (authorDetails) {
    //         navigate(`/profile`, { state: { author: authorDetails } });
    //     } else {
    //         console.error('Author details are not available');
    //     }
    // };

    const extractUUIDFromURL = (url) => {
        const parts = url.split('/');
        let uuid = parts.pop();
        if (uuid === '') uuid = parts.pop();
        return uuid;
    }

    const getAllUsers = () => {
        axiosInstance.get("authors/user")
            .then(response => {
                const filteredUsers = response.data.items.filter(user => extractUUIDFromURL(user.id) !== userId);
                setAllUsers(filteredUsers);
            })
            .catch(error => console.error('Error fetching users:', error));
    };

    const fetchLikes = () => {
        const postAuthorId = extractUUIDFromURL(authorDetails.id);
        const likeUrl = `authors/${postAuthorId}/posts/${post.post_id}/like/`;
        axiosInstance.get(likeUrl)
            .then(response => {
                const likeItems = response.data.items || [];
                console.log('this are the likes for  post', response.data.items)
                // setLikeCount(response.data.items.length)
                setLikesCount(likeItems.length);
                setLiked(likeItems.some(like => like.author.id === storedUser.url));
            })
            .catch(error => console.error('Error fetching likes:', error));
    };

    const handleLike = () => {

        const loggedInUserId = extractUUIDFromURL(loggedINUser.user.id);
        const likeUrl = `authors/${loggedInUserId}/posts/${post.post_id}/like/`;

        if (liked) {
            axiosInstance.delete(likeUrl)
                .then(() => {
                    setLiked(false);
                    fetchLikes();
                })
                .catch(error => console.error('Error unliking post:', error));
        } else {
            const likesData = {
                author: storedUser,
                type: "like",
                summary: `${storedUser.displayName} Likes your post`,
                object: post.url
            };
            axiosInstance.post(likeUrl, likesData)
                .then(() => {
                    setLiked(true);
                    fetchLikes();
                })
                .catch(error => console.error('Error liking post:', error));
        }
    };


    const handleShare = () => {
        setOpenModal(true);
        setModalMode('Share');
    };

    const handleEdit = () => {
        setOpenModal(true);
        setModalMode('edit');
    };

    const handleComment = () => {
        setOpenModal(true);
        setModalMode('comment')
    }

    return (
        <div className="card">
            <div className="edit-container">
                <button onClick={handleEdit} className={`edit-button ${canEdit ? "" : "invisible"}`}>
                    <img src={editIcon} alt="Edit" />
                </button>
            </div>


            <div className="card-body">
                <h2 className="card-title">{post.title}</h2>
            </div>


            <div className="footer-container">
                <div className="userNamePost">
                    {console.log('person who made post', authorDetails)}
                    {authorDetails?.displayName && (
                        <span>
                            {authorDetails.displayName}
                        </span>
                    )}
                </div>
                <div className="card-footer">
                    <span className="like-count">{likesCount}</span>
                    {liked ? (
                        <>

                            <FavoriteIcon onClick={handleLike} style={{ fontSize: '40px', color: 'red', cursor: 'pointer', marginRight: '10px' }} />


                        </>

                    ) : (
                        <FavoriteBorderOutlinedIcon onClick={handleLike} style={{ fontSize: '40px', cursor: 'pointer', marginRight: '10px' }} />
                    )}
                    <ChatBubbleOutlineIcon onClick={handleComment} style={{ fontSize: '40px', cursor: 'pointer', marginRight: '10px' }} />
                    <ShareOutlinedIcon onClick={handleShare} style={{ fontSize: '40px', cursor: 'pointer' }} />
                </div>
                {openModal && <Modal isOpen={openModal} mode={modalMode} users={allusers} post={post} onClose={() => setOpenModal(false)} />}
            </div>
        </div>
    );
}
