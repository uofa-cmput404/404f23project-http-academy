import { useEffect, useState } from "react"
import '../css/InboxDetail.css'
const InboxDetail = ({ item }) => {
    if (item.type === "Like") {
       
        return (
            <div className="item-inboxDetail">
                <img src={item.author.profileImage} alt="Preview" style={{ width: '100px', height: '100px' }} />
                <h1>{item.summary}</h1>
               
            </div>
        );
    } else if (item.type === "Follow") {
       
        return (
            <div className="item-inboxDetail">
                <img src={item.profileImage} alt="Preview" style={{ width: '100px', height: '100px' }} />
                <h1>{item.summary}</h1>
               
            </div>
        );
    } else {
        
    }
};

export default InboxDetail;

