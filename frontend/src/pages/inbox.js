import InboxDetail from '../components/InboxDetail';
import { useState , useEffect} from 'react';
import '../css/inbox.css';
import Button from '@mui/material/Button';

const Inbox = () => {
    const [InboxItems, setInboxItems] = useState([/* your static data here */]);
    const [activeTab, setActiveTab] = useState("liked");
    const inbox = [{


      
        "type":"liked",
        "items":[
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "summary": "Lara Croft Likes your post",         
                "type": "Like",
                "author":{
                    "type":"author",
                    "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    "host":"http://127.0.0.1:5454/",
                    "displayName":"Lara Croft",
                    "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    "github":"http://github.com/laracroft",
                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                },
                "object":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
            }
        ]
    },

    {


  
        "type":"liked",
        "items":[
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "summary": "Lara Croft Likes your post",         
                "type": "Like",
                "author":{
                    "type":"author",
                    "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    "host":"http://127.0.0.1:5454/",
                    "displayName":"Lara Croft",
                    "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    "github":"http://github.com/laracroft",
                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                },
                "object":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
            }
        ]
    },
    {


  
        "type":"follow",
        "items":[
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "summary": "Greg wants to follow lara",         
                "type": "Like",
                "author":{
                    "type":"author",
                    "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    "host":"http://127.0.0.1:5454/",
                    "displayName":"Lara Croft",
                    "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    "github":"http://github.com/laracroft",
                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                },
                "object":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
            }
        ]
    },



    ]


    useEffect(() => {
        // getInbox();
        setInboxItems(inbox)
    }, [])

    return (
        <div>
            <h1>INBOX</h1>
            
            <div className='inbox-header'>
                <h2 className={`item1 ${activeTab === "liked" ? "active2" : ""}`} onClick={() => setActiveTab("liked")}>Posts</h2>
                <h2 className={`item2 ${activeTab === "follow" ? "active2" : ""}`} onClick={() => setActiveTab("follow")}>Friend Requests</h2>
            </div>
            {
                InboxItems.filter(inboxItem => inboxItem.type === activeTab).map((inboxItem, index) => (
                    inboxItem.items.map(item => (
                        <InboxDetail key={`${index}-${item.id}`} item={item} />
                    ))
                ))
            }
        </div>
    );
};

export default Inbox;
