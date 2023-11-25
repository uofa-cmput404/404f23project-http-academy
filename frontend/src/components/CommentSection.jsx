

import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axiosInstance from '../axiosInstance';
import Comment from './Comment';
import '../css/CommentSection.css'
import { extractUUIDFromURL } from '../utilities/extractUIID';
import FavoriteIcon from '@mui/icons-material/Favorite';
import FavoriteBorderOutlinedIcon from '@mui/icons-material/FavoriteBorderOutlined';
import { FormControl, TextField, Button, InputLabel, MenuItem, Paper, Select, Divider, List, ListItem, ListItemText } from "@mui/material";
var ReactCommonmark = require('react-commonmark');

export default function CommentSection({ postid }) {
  const [localComments, setLocalComments] = useState([]);
  const storedUser_val = JSON.parse(localStorage.getItem('user'));
  const storedUser = storedUser_val.user;
  const userId = storedUser.id.split("/").pop();
  const [commentText, setCommentText] = useState('');
  const [inputType, setInputType] = useState("");
  const [newUserComment, setNewUserComment] = useState("");
  const [allusers, setAllUsers] = useState([])
  const [likedComments, setLikedComments] = useState({});
  const [commentLikeCounts, setCommentLikeCounts] = useState({});
  const { id } = useParams();

  useEffect(() => {
    fetchAllUsers();
    fetchComments();
  }, [userId, postid]);

  useEffect(() => {
    localComments.forEach(comment => {
      fetchCommentLikes(comment.id.split('/').pop());
    });
  }, [localComments]);

  const findUserDisplayName = (uuid) => {
    console.log('all users', allusers)
    const user = allusers.find(user => extractUUIDFromURL(user.id) === uuid);
    console.log('i found user', user)
    return user ? user.displayName : "Unknown User";
  };


  const fetchCommentLikes = (commentId) => {
    const commentsUrl = `authors/${userId}/posts/comments/${commentId}/likes/`;
    axiosInstance.get(commentsUrl)
      .then(response => {
        console.log('my likes from the backend', response);

        const isLiked = response.data ? response.data.some(like => like.author_id === userId) : false;
        const likeCount = response.data ? response.data.length : 0;
        setLikedComments(prevLikes => ({
          ...prevLikes,
          [commentId]: isLiked
        }));
        console.log('set liked comments', likedComments)
        setCommentLikeCounts(prevCounts => ({
          ...prevCounts,
          [commentId]: likeCount
        }));
      })
      .catch(error => console.error('Error fetching comment likes:', error));
  };

  const handleLikeComment = (commentId) => {
    const likeUrl = `authors/${userId}/posts/comments/${commentId}/likes/`;
    axiosInstance.post(likeUrl, { author: userId })
      .then(() => {
        setLikedComments(prevLikes => ({
          ...prevLikes,
          [commentId]: true
        }));
        setCommentLikeCounts(prevCounts => ({
          ...prevCounts,
          [commentId]: (prevCounts[commentId] || 0) + 1
        }));
      })
      .catch(error => console.error('Error liking comment:', error));
  };

  const handleUnlikeComment = (commentId) => {
    const likeUrl = `authors/${userId}/posts/comments/${commentId}/likes/`;
    axiosInstance.delete(likeUrl)
      .then(() => {
        setLikedComments(prevLikes => ({
          ...prevLikes,
          [commentId]: false
        }));
        setCommentLikeCounts(prevCounts => ({
          ...prevCounts,
          [commentId]: (prevCounts[commentId] || 1) - 1
        }));
      })
      .catch(error => console.error('Error unliking comment:', error));
  };



  const renderLikeButton = (commentId) => {
    const likeCount = commentLikeCounts[commentId] ?? 0;
    const likeButton = likedComments[commentId] ? (
      <FavoriteIcon onClick={() => handleUnlikeComment(commentId)} style={{ fontSize: '40px', color: 'red', cursor: 'pointer', marginRight: '10px' }} />
    ) : (
      <FavoriteBorderOutlinedIcon onClick={() => handleLikeComment(commentId)} style={{ fontSize: '40px', cursor: 'pointer', marginRight: '10px' }} />
    );

    return (
      <div style={{ display: 'flex', alignItems: 'center' }}>
        {likeButton}
        <span>{likeCount}</span>
      </div>
    );
  };



  const fetchAllUsers = () => {
    axiosInstance.get("authors/user")
      .then(response => {

        console.log('filters user showing', response.data.items)
        setAllUsers(response.data.items);
      })
      .catch(error => console.error('Error fetching users:', error));
  };

  const addComment = () => {
    const commentUrl = `authors/${userId}/posts/${postid}/comments/`;
    const publishTime = new Date();
    let content = commentText;


    if (inputType === "image/png;base64" || inputType === "image/jpeg;base64" || inputType === "application/base64") {
      content = newUserComment;
    }

    const commentData = {
      type: "comment",
      author: userId,
      comment: content,
      contentType: inputType,
      published: publishTime.toISOString()
    };

    console.log('current comment data', userId, postid);

    const commentsUrl = `authors/${userId}/posts/${postid}/comments/`;
    axiosInstance.post(commentsUrl, commentData)
      .then(response => {
        fetchComments();
        setCommentText('');
        console.log('this are the cpmments for  post', response.data.items)

      })
      .catch(error => console.error('Error fetching comments:', error));

  };

  const fetchComments = () => {
    const commentingUrl = `authors/${userId}/posts/${postid}/comments/`;

    const commentsUrl = `authors/${userId}/posts/${postid}/comments/`;
    console.log('request logegd for get cmmand', commentsUrl)
    console.log('request logegd for get cmmand 2', userId, postid)
    axiosInstance.get(commentsUrl)
      .then(response => {
        console.log('Fetched comments:', response.data);
        setLocalComments(response.data);


      })
      .catch(error => console.error('Error fetching comments:', error));

  };

  const handleInputTypeChange = (event) => {
    setInputType(event.target.value);
  };

  const checkTypeOfComment = (val) => {
    if (val.contentType === "text/markdown") {
      return (<ListItemText primary={<ReactCommonmark source={val.comment} />} secondary={val.author.displayName} />);
    } else if (val.contentType === "text/plain") {
      return (<ListItemText primary={val.comment} secondary={val.author.displayName} />);
    }
  }

  const handleImageUpload = (event) => {
    const fileUploaded = event.target.files[0];
    const reader = new FileReader();
    reader.readAsDataURL(fileUploaded);
    reader.onload = () => {
      setNewUserComment(reader.result.split(',')[1]);
    };
  };

  const hiddenFileInput = React.useRef(null);

  const handleBtnSelection = () => {
    hiddenFileInput.current.click();
  }

  const renderComment = (val) => {
    let commentContent;
    console.log('val ', val)
    let displayName = findUserDisplayName(val.author);

    console.log('display name should render', displayName)
    if (val.contentType === "text/markdown") {
      commentContent = <ReactCommonmark source={val.comment} />;
    } else if (val.contentType === "text/plain") {
      commentContent = val.comment;
    } else if (val.contentType.includes("base64")) {
      commentContent = <img src={`data:${val.contentType};base64,${val.comment}`} alt="Comment" />;
    }

    return (
      <React.Fragment>
        <div className="commentText">{commentContent}</div>
        <div className="authorDisplayName">{displayName}</div>
      </React.Fragment>
    );
  };


  return (
    <div>
      <div className='comment-contains'>
        <div className='flex-comment'>
          <h2>Make a <br></br>Comment</h2>
        </div>

        <div className="formElement">
          <FormControl fullWidth>
            <InputLabel id="demo-simple-select-label">Choose Comment Type</InputLabel>
            <Select
              labelId="demo-simple-select-label"
              value={inputType}
              label="Input Type"
              onChange={handleInputTypeChange}
            >
              <MenuItem value={"text/markdown"}>text/markdown</MenuItem>
              <MenuItem value={"text/plain"}>text/plain</MenuItem>
              <MenuItem value={"application/base64"}>application/base64</MenuItem>
              <MenuItem value={"image/png;base64"}>image/png;base64</MenuItem>
              <MenuItem value={"image/jpeg;base64"}>image/jpeg;base64</MenuItem>
            </Select>
          </FormControl>
        </div>
      </div>

      <div className='commentSection-container'>
        <List className="commentList">
          {console.log('local commentig ', localComments)}
          {localComments.map((val) => (
            <ListItem key={val.id} className="commentItem" disableGutters>
              {renderComment(val)}
              {renderLikeButton(val.id.split('/').pop())}
            </ListItem>
          ))}
        </List>

        <div>
          {inputType === "image/png;base64" || inputType === "image/jpeg;base64" || inputType === "application/base64" ?
            <div className="UploadImage">
              <Button variant="contained" component="label" onClick={handleBtnSelection}>
                Upload Image
                <input type="file" ref={hiddenFileInput} onChange={handleImageUpload} hidden />
              </Button>
            </div>
            : ""
          }
        </div>
        <div>
          {inputType === "text/plain" || inputType === "text/markdown" ?
            <TextField
              multiline
              autoFocus
              margin="dense"
              id="name"
              label="Add Comment"
              type="comment"
              fullWidth
              variant="standard"
              onChange={(e) => setCommentText(e.target.value)}
            />
            : ""
          }
        </div>

      </div>
      <Button onClick={addComment}>Post Comment</Button>
    </div>

  )
}