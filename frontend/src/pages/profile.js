import React, { useEffect, useState } from "react";
import "../css/Profile.css";
import axiosInstance from "../axiosInstance";

const Profile = () => {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [editMode, setEditMode] = useState(false);
  const [error, setError] = useState("");

  // const storedUser = JSON.parse(localStorage.getItem('user'));
  const [userid, setUserID] = useState(0);
  useEffect(() => {
    const handleStorageChange = () => {
      const storedUser = JSON.parse(localStorage.getItem('user'));
      console.log(storedUser);
      if (storedUser) {
        setEmail(storedUser.email);
        setUsername(storedUser.username);
        setUserID(storedUser.id);
      }
    };

    window.addEventListener('storage', handleStorageChange);

    // Call the function to make sure the user is updated when the component mounts
    handleStorageChange();

    return () => {
      // Remove the event listener when the component unmounts
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  const handleUpdate = async () => {
    if (!email || !username) {
      setError("Please fill out all fields.");
      return;
    }

    axiosInstance
      .patch(`authors/${userid}/update/`, {
        username,
        email,
      })
      .then((response) => {
        console.log('server response', response);
        localStorage.setItem('user', JSON.stringify(response.data));
        setEditMode(false);
        setError("");
      })
      .catch((error) => {
        console.log('Error updating profile', error);
        setError("An error occurred while updating your profile.");
      });

  };

  return (
    <div className="profile-container">
      <div className="profile-card">
        {editMode ? (
          <div>
            <div className="profile-header">Edit Profile</div>
            <label className="profile-label">
              Username:
              <input
                className="profile-input"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </label>
            <br />
            <label className="profile-label">
              Email:
              <input
                className="profile-input"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </label>
            <br />
            <button className="profile-button" onClick={handleUpdate}>
              Update
            </button>
            <button className="profile-button profile-button-cancel" onClick={() => setEditMode(false)}>
              Cancel
            </button>
          </div>
        ) : (
          <div>
            <div className="profile-header">Profile</div>
            USERNAME: <h2>{username}</h2>
            Email: <h2>{email}</h2>
            <button className="profile-button" onClick={() => setEditMode(true)}>
              Edit
            </button>
          </div>
        )}
        {error && <p className="profile-error">{error}</p>}
      </div>
    </div>

  );
};

export default Profile;
