import React, { useState, useEffect } from "react";
import axiosInstance from "../axiosInstance";
import '../css/Search.css';

export default function Search({ setPosts, findAuthorForPost, oldPosts }) {
  const [searchQuery, setSearchQuery] = useState('');

  const handlePostSearch = () => {
    try {
      axiosInstance.get(`posts/search/${searchQuery}/`)
        .then(response => {
          const posts = response.data;
          const postsWithAuthors = posts.map(post => ({
            ...post,
            authorDetails: findAuthorForPost(post)
          }));
          setPosts(postsWithAuthors);
        })
        .catch(error => console.error(error));
    }
    catch (e) {
      console.log(e);
    }
  };

  useEffect(() => {
    if (searchQuery.trim() === '') {
      setPosts(oldPosts);
      console.log(oldPosts);
    } else {
      handlePostSearch();
      console.log(oldPosts);
    }
  }, [searchQuery, oldPosts, setPosts]);

  const handleChange = (event) => {
    setSearchQuery(event.target.value);
    if (searchQuery === '') {
      setPosts(oldPosts);
    }
  };

  return (
    <div className="search-container">
      <input
        type="text"
        placeholder="Start typing to search"
        value={searchQuery}
        onChange={handleChange}
      />
    </div>
  );
}