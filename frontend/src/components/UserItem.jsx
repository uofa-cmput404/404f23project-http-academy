const UserItem = ({ user }) => (
    <div className='user-item'>
        <img src={user.profileImage || 'default-profile.png'} alt="Profile" />
        <p>{user.displayName}</p>
    </div>
);

export default UserItem;