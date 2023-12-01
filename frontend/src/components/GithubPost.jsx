import React, { useEffect, useState } from 'react';
import axios from 'axios';
import isGithubUrl from 'is-github-url';
import "../css/Post.css";

const GitHubPost = ({ githubUrl }) => {
    const [activities, setActivities] = useState([]);

    useEffect(() => {
        console.log('came here to render github', githubUrl)
        if (githubUrl && isGithubUrl(githubUrl)) {
            const username = new URL(githubUrl).pathname.slice(1);
            const apiURL = `https://api.github.com/users/${username}/events/public?per_page=6`
            console.log('api url', apiURL)
            fetch(apiURL)
                .then(response => response.json())
                .then(data => {
                    const formattedActivities = data.map(({ actor, type, repo, created_at }) => ({
                        user: actor.display_login,
                        type: type,
                        repo: repo.name,
                        created_at: created_at
                    }));
                    const activitiesChunks = chunkActivities(formattedActivities, 3);
                    setActivities(activitiesChunks);
                    console.log('formatted activities', formattedActivities)
                })
                .catch(error => console.error('Error fetching GitHub data:', error));
            // axios.get(apiURL)
            //     .then(response => {
            //         console.log('activities', response.data)

            //         setActivities(formattedActivities);
            //     })
            //     .catch(error => console.error('Error fetching GitHub data:', error));
        }
    }, [githubUrl]);


    const chunkActivities = (activities, chunkSize) => {
        return activities.reduce((resultArray, item, index) => {
            const chunkIndex = Math.floor(index / chunkSize);
            if (!resultArray[chunkIndex]) {
                resultArray[chunkIndex] = []; // Start a new chunk
            }
            resultArray[chunkIndex].push(item);
            return resultArray;
        }, []);
    };


    return (
        <div>
            {activities.map((chunk, chunkIndex) => (
                <div key={chunkIndex} className="posts-row">
                    {chunk.map((activity, index) => (
                        <div key={index} className="card" >
                            <div className="card-body" style={{
                                // "background-color": "red"
                            }}>
                                <h3>{activity.user}</h3>
                                <p>{activity.type} - {activity.repo}</p>
                                <small>{activity.created_at}</small>
                            </div>
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );

};

export default GitHubPost;


