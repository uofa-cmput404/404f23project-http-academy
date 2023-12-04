import React, { useState, useEffect, useCallback } from "react";
import axiosInstance from "../axiosInstance";
import '../css/Search.css';

export default function Search({ setPosts, findAuthorForPost, oldPosts }) {
  const [searchQuery, setSearchQuery] = useState('');

  const handlePostSearch = useCallback(() => {
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
    } catch (e) {
      console.log(e);
    }
  }, [searchQuery, setPosts, findAuthorForPost]);

  useEffect(() => {
    if (searchQuery.trim() === '') {
      setPosts(oldPosts);
    } else {
      handlePostSearch();
    }
  }, [searchQuery, oldPosts, setPosts, handlePostSearch]);

  const handleChange = (event) => {
    setSearchQuery(event.target.value);
    if (event.target.value === '') {
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
