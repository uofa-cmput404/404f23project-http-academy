
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../css/MakePost.css";
import axiosInstance from "../axiosInstance";

export default function MakePr() {

    const defaultPosts = [
        {title: "Test", body: "Body"},
        {title: "Test", body: "Body"},
        {title: "Test", body: "Body"},
        {title: "Test", body: "Body"},
    ];

    axiosInstance.post('posts/', defaultPosts
    ).then(response => {
        console.log(response);
    }).catch(error => {
        console.log(error);
    });
}

