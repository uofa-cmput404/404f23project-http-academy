import React, { useEffect, useState, useCallback } from "react";
import "../css/Profile.css";
import axiosInstance from "../axiosInstance";
// import { useLocation } from "react-router-dom";
import { Button, Avatar } from "@mui/material";
import { yellow } from "@mui/material/colors";
import Typography from '@mui/material/Typography';
import { extractUUIDFromURL } from "../utilities/extractUIID";
import Post from '../components/Post';
import GitHubPost from "../components/GithubPost";

const Profile = () => {


  const [followers, setFollowers] = useState([]);
  const [postsowned, setPostsOwned] = useState([])
  const [following, setFollowing] = useState([]);
  const storedUser_val = JSON.parse(localStorage.getItem('user'));
  const storedUser = storedUser_val.user
  const userId = storedUser.id.split("/").pop()
  const [githubUrl, setGithubUrl] = useState('');



  useEffect(() => {
    const githubUrl = storedUser.github;
    setGithubUrl(githubUrl);
  }, [])

  const handleUnfriend = (requesterId) => {

    const url = `authors/${userId}/followers/removeFriend/${requesterId}/`;
    axiosInstance.delete(url, { user_id: userId, requesterId: requesterId })
      .then(response => {
        // Refresh the followers and following list after made unfrined user
        fetchFollowers();
        fetchFollowing();
      })
      .catch(error => {
        console.error('Error unfriending user:', error);
      });
  };

  const fetchFollowers = useCallback(() => {
    axiosInstance.get(`/authors/${userId}/followers`)
      .then(response => {
        setFollowers(response.data.items);
      })
      .catch(error => {
        console.error('Error fetching followers:', error);
      });
  }, [userId]);

  const fetchFollowing = useCallback(() => {
    axiosInstance.get(`/authors/${userId}/following`)
      .then(response => {
        setFollowing(response.data.items);
      })
      .catch(error => {
        console.error('Error fetching following:', error);
      });
  }, [userId]);

  const fetchPosts = useCallback(() => {

    const url = `authors/${userId}/posts/ownPosts/`;
    axiosInstance.get(url).then(response => {
      const Posts = response.data.items
      const postsWithAuthors = Posts.map(post => ({
        ...post,
      }));
      setPostsOwned(postsWithAuthors);
    }).catch(error => {
      console.log(error);
    });
  }, [userId]);

  useEffect(() => {
    fetchFollowers();
    fetchFollowing();
    fetchPosts();
  }, [userId, fetchFollowers, fetchFollowing, fetchPosts]);






  const checkProfImageExist = (user) => {
    const userProfileUrl = user.profileImage;
    const userName = user.displayName;
    const hasImage = userProfileUrl && userProfileUrl.match(/\.(jpeg|jpg|gif|png)$/);
    const avatarStyle = { width: 100, height: 100 };
    const githubUsername = githubUrl.split('/').pop();
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', marginTop: "40px" }}>
        {hasImage ? (
          <Avatar alt={userName} src={userProfileUrl} style={avatarStyle} />
        ) : (
          <Avatar sx={{ bgcolor: yellow[500], ...avatarStyle }}>
            {userName ? userName[0] : '?'}
          </Avatar>
        )}
        <Typography variant="body1" style={{ fontSize: "40px", fontWeight: "bold", marginTop: '10px', textAlign: 'center', width: '100px' }}>
          {userName}
        </Typography>
        {githubUsername && (
          <a href={githubUrl} target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none', color: '#7D633C' }}>
            @{githubUsername}
          </a>
        )}
      </div>
    );
  };

  // const renderPosts = (item) => {
  //   console.log('rendering posts', item)
  //   // return(
  //   //   <Post key={item.id} post={item} canEdit={userId === item.author} authorDetails={item.authorDetails} />
  //   // )
  // }


  return (
    <div>
      <div className="profile-contain">
        <h1>PROFILE</h1>
      </div>
      <div className="full-containr">
        <div className="profile-inContainer">
          <div>
            {checkProfImageExist(storedUser)}
          </div>
          <div className="listsContainer">
            <div className="followersList">
              <h2>Followers</h2>
              {followers.map(follower => (
                <div key={follower.id} className="follower-item">
                  <p>{follower.displayName}</p>
                  <Button onClick={() => handleUnfriend(extractUUIDFromURL(follower.id))}>
                    Unfriend
                  </Button>
                </div>
              ))}
            </div>
            <div className="followingList">
              <h2>Following</h2>
              {following.map(follow => (
                <div key={follow.id} className="following-item">
                  <p>{follow.displayName}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="post-section">
          <div className="post-heading">
            <h1>Posts</h1>
            {postsowned.map(item => (
              <Post key={item.post_id} post={item} canEdit={userId === item.author} authorDetails={storedUser} />

            ))}
          </div>


        </div>
      </div>


    </div>
  );




};

export default Profile;

