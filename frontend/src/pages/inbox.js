// import React, { useEffect, useState } from 'react';
// import axiosInstance from '../axiosInstance';
// import Button from '@mui/material/Button';
// import '../css/inbox.css';
// import FriendRequestItem from '../components/FriendRequestItem';
// import Post from '../components/Post';

// const Inbox = () => {
//     console.log('inbox component rendered')
//     const [inboxItems, setInboxItems] = useState({ follow_request: [] }); // Ensure initial state is an object with a follow_request array
//     const [activeTab, setActiveTab] = useState("liked");
//     const currentUser = JSON.parse(localStorage.getItem('user'));
//     const currentUserId = currentUser.id;
//     const [posts, setPosts] = useState([]);
//     const [allUsers, setAllUsers] = useState([])

//     useEffect(() => {
        

//         // fetchInbox();
        
//         axiosInstance.get('authors/user').then(response => {
                
//                 const usersWithProcessedIds = response.data.items.map(user => ({
//                     ...user,
//                     numericId: extractIdFromUrl(user.id)
//                 }));
//                 {console.log('it workss', usersWithProcessedIds)}
        
//                 setAllUsers(usersWithProcessedIds)
//                 fetchInbox();
//             }).catch(error => {
//                 console.error('Error fetching users', error);
//             });
        
//     }, [currentUserId]);


//     const extractIdFromUrl = (url) => {
//         const segments = url.split('/');
//         return segments[segments.length - 1];
//     };
    
//     const findAuthorForPost = (post) => {

//         const author = allUsers.find(user => user.numericId === post.author.toString());
//         console.log('Author for post:', author);
//         return author;
//     };

    
   
    
    

//     const fetchInbox = () => {
//         // console.log('got hererer')



//         axiosInstance.get(`authors/${currentUserId}/inbox/`).then(response => {
//             const postsWithAuthors = response.data.posts.map(post => ({
//                 ...post,
//                 authorDetails: findAuthorForPost(post)
//             }));
//             setInboxItems({...response.data, posts: postsWithAuthors});
//             console.log('ogo', inboxItems)
            
//         }).catch(error => {
//             console.error('Error fetching users', error);
//         });

   
//     };
    
    

//     const confirmFriendRequest = async (senderId, receiverId) => {
//         try {
//             const response = await axiosInstance.post(`authors/${currentUserId}/followers/acceptFriendRequest/${receiverId}/${senderId}/`);
            
            
//             setInboxItems(prevItems => {
//                 const updatedRequests = prevItems.follow_request.map(item => {
//                     if (item.actor.user_id === senderId && item.object.user_id === receiverId) {
                        
//                         return { ...item, accepted: true }; 
//                     }
//                     return item;
//                 });
    
//                 return { ...prevItems, follow_request: updatedRequests };
//             });
    
//         } catch (error) {
//             console.error('Error confirming friend request', error);
//         }
//     };
    

//     const establishMutualFriendship = async (friendId) => {
//         try {
//             await axiosInstance.post(`authors/${currentUserId}/followers/establishMutualFriendship/${currentUserId}/${friendId.toString()}/`);
//         } catch (error) {
//             console.error('Error establishing mutual friendship', error);
//         }
//     };

//     const renderPosts = () => {
//         return (
//             <div>
//                 {console.log('items in inbix',inboxItems)}
//                 {inboxItems.posts.map((post, index) => (
//                     <Post 
//                         key={index}
//                         post={post}
//                         canEdit={currentUserId === post.author}
//                         authorDetails={post.authorDetails}
//                     />
//                 ))}
//             </div>
//         );
//     };
    
    
    

//     const renderFriendRequests = () => {
//         return (
//             <div>
//                 {inboxItems.follow_request.map(request => (
//                     <FriendRequestItem 
//                         key={request.id}
//                         request={request}
//                         confirmFriendRequest={confirmFriendRequest}
//                         establishMutualFriendship={establishMutualFriendship}
//                     />
//                 ))}
//             </div>
//         );
//     };


//     return (
//         <div className='inbox-outer-container'>
//             <h1>INBOX</h1>
//             <div className='inbox-header'>
//                 <h2 className={`item1 ${activeTab === "posts" ? "active2" : ""}`} onClick={() => setActiveTab("posts")}>Posts</h2>
//                 <h2 className={`item2 ${activeTab === "follow" ? "active2" : ""}`} onClick={() => setActiveTab("follow")}>Friend Requests</h2>
//             </div>
//             <div className='follow_container'>
//                 {activeTab === "follow" && renderFriendRequests()}
//                 {activeTab === "posts" && renderPosts()} 
//             </div>
//         </div>
//     );
    
    
// };

// export default Inbox;


import React, { useEffect, useState } from 'react';
import axiosInstance from '../axiosInstance';
import '../css/inbox.css';
import FriendRequestItem from '../components/FriendRequestItem';
import Post from '../components/Post';

const Inbox = () => {
    console.log('inbox component rendered');
    const [friendRequests, setFriendRequests] = useState([]);
    const [posts, setPosts] = useState([]);
    const [activeTab, setActiveTab] = useState("posts");
    const currentUser = JSON.parse(localStorage.getItem('user'));
    const currentUserId = currentUser.id;
    const [allUsers, setAllUsers] = useState([]);

    useEffect(() => {
        fetchAllUsers();
    }, [currentUserId]);

    const extractIdFromUrl = (url) => {
        const segments = url.split('/');
        return segments[segments.length - 1];
    };

    const findAuthorForPost = (post) => {
        return allUsers.find(user => user.numericId === post.author.toString());
    };

    const fetchAllUsers = () => {
        axiosInstance.get('authors/user').then(response => {
            const usersWithProcessedIds = response.data.items.map(user => ({
                ...user,
                numericId: extractIdFromUrl(user.id)
            }));
            setAllUsers(usersWithProcessedIds);
            fetchInbox();
        }).catch(error => {
            console.error('Error fetching users', error);
        });
    };

    const fetchInbox = () => {
        axiosInstance.get(`authors/${currentUserId}/inbox/`).then(response => {
            const inboxData = response.data;
            const postsWithAuthors = inboxData.posts.map(post => ({
                ...post,
                authorDetails: findAuthorForPost(post)
            }));
            setPosts(postsWithAuthors);
            setFriendRequests(inboxData.follow_request);
        }).catch(error => {
            console.error('Error fetching inbox', error);
        });
    };

    const confirmFriendRequest = async (senderId, receiverId) => {
        try {
            await axiosInstance.post(`authors/${currentUserId}/followers/acceptFriendRequest/${receiverId}/${senderId}/`);
            setFriendRequests(prevRequests => prevRequests.map(request => {
                if (request.actor.user_id === senderId && request.object.user_id === receiverId) {
                    return { ...request, accepted: true };
                }
                return request;
            }));
        } catch (error) {
            console.error('Error confirming friend request', error);
        }
    };

    const establishMutualFriendship = async (senderId, receiverId) => {
        console.log('mutual', senderId, receiverId)
        try {
            await axiosInstance.post(`authors/${currentUserId}/followers/establishMutualFriendship/${receiverId}/${senderId}/`);
        } catch (error) {
            console.error('Error establishing mutual friendship', error);
        }
    };

    const renderPosts = () => (
        <div className='post-contain'>
            {posts.map((post, index) => (
                <Post key={index} post={post} canEdit={currentUserId === post.author} authorDetails={post.authorDetails} />
            ))}
        </div>
    );

    const renderFriendRequests = () => (
        <div>
            {friendRequests.map(request => (
                <FriendRequestItem key={request.id} request={request} confirmFriendRequest={confirmFriendRequest} establishMutualFriendship={establishMutualFriendship} />
            ))}
        </div>
    );

    return (
        <div className='inbox-outer-container'>
            <h1>INBOX</h1>
            <div className='inbox-header'>
                <h2 className={`item1 ${activeTab === "posts" ? "active2" : ""}`} onClick={() => setActiveTab("posts")}>Posts</h2>
                <h2 className={`item2 ${activeTab === "follow" ? "active2" : ""}`} onClick={() => setActiveTab("follow")}>Friend Requests</h2>
            </div>
            <div className='follow_container'>
                {activeTab === "follow" && renderFriendRequests()}
                {activeTab === "posts" && renderPosts()} 
            </div>
        </div>
    );
};

export default Inbox;
