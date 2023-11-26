import React, { useState } from 'react';
import { Button } from '@mui/material';

const FriendRequestItem = ({ request, confirmFriendRequest, establishMutualFriendship }) => {
    const [followBackCompleted, setFollowBackCompleted] = useState(false);

    const handleFollowBack = async (actorId, objectId) => {
        await establishMutualFriendship(actorId, objectId);
        setFollowBackCompleted(true);
    };

    return (
        <div className='request_list'>
            {request.actor.profileImage && <img src={request.actor.profileImage} alt="Profile" />}
            <p>{request.summary}</p>
            <div className='confirm_req_container'>
                {request.type === "Follow" && !request.accepted ? (
                    <>
                        <Button onClick={() => confirmFriendRequest(request.actor.user_id, request.object.user_id)}
                                className="accept_req" variant="contained">Confirm</Button>
                        <Button className="deny_req" variant="contained">Deny</Button>
                    </>
                ) : request.type === "Notification" ? (
                    <p>{request.summary}</p>
                ) : (
                    !followBackCompleted && (
                        <Button onClick={() => handleFollowBack(request.actor.user_id, request.object.user_id)}
                                className="follow_back_req" variant="contained">Follow Back</Button>
                    )
                )}
            </div>
        </div>
    );
};

export default FriendRequestItem;
