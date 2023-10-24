import axios from 'axios'
const baseUrl = 'http://localhost:3001/posts'


//get multiple posts
const getAll = () => {
    const request = axios.get(baseUrl)
    return request.then(response => {
        return response.data
      })
}

//get single post
const get = (id) => {
    const request = axios.get(`${baseUrl}/${id}`);
    return request.then(response => {
        return response.data
      })
};

//create single post
const create = newObject => {
    const request = axios.post(baseUrl, newObject)
    return request.then(response => {
        return response.data
      })
}

//update post
const update = (id, newObject) => {
    const request = axios.put(`${baseUrl}/${id}`, newObject)
    return request.then(response => {
        return response.data
      })
}


const remove = (id) => {
    const request = axios.delete(`${baseUrl}/${id}`);
    return request.then(response => response.data);
  };
  
  export default {
    getAll,
    create, 
    update,
    get,
    remove 
  };