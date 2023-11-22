
export const extractUUIDFromURL = (url) => {
    const parts = url.split('/');
    let uuid = parts.pop();
    if (uuid === '') uuid = parts.pop();
    return uuid;
}
