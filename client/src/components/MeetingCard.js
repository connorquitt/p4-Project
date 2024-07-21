import React, { useState } from 'react';
import '../index.css'; // Adjust the path as necessary
import { NavLink } from 'react-router-dom';

function MeetingCard({ meeting, onDelete, onUpdate }) {
    const [isEditing, setIsEditing] = useState(false);
    const [newTopic, setNewTopic] = useState(meeting.topic);
    const [newScheduledTime, setNewScheduledTime] = useState(meeting.scheduled_time);
    const [newLocation, setNewLocation] = useState(meeting.location);

    const handleDelete = () => {
        fetch(`/meetings/${meeting.id}`, {
            method: 'DELETE',
        })
        .then((response) => {
            if (response.ok) {
                onDelete(meeting.id);
            }
        })
        .catch((error) => {
            console.error('Error deleting meeting:', error);
        });
    };

    const handleEdit = () => {
        setIsEditing(true);
    };

    const handleSave = () => {
        fetch(`/meetings/${meeting.id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                topic: newTopic,
                scheduled_time: newScheduledTime,
                location: newLocation,
            }),
        })
        .then((response) => response.json())
        .then((updatedMeeting) => {
            onUpdate(updatedMeeting);
            setIsEditing(false);
        })
        .catch((error) => {
            console.error('Error updating meeting:', error);
        });
    };

    return (
        <div key={meeting.id} className="card">
            {isEditing ? (
                <div>
                    <input
                        type="text"
                        value={newTopic}
                        onChange={(e) => setNewTopic(e.target.value)}
                        placeholder="Topic"
                    />
                    <input
                        type="datetime-local"
                        value={newScheduledTime}
                        onChange={(e) => setNewScheduledTime(e.target.value)}
                    />
                    <input
                        type="text"
                        value={newLocation}
                        onChange={(e) => setNewLocation(e.target.value)}
                        placeholder="Location"
                    />
                    <button onClick={handleSave}>Save</button>
                </div>
            ) : (
                <div>
                    <h3>Topic: {meeting.topic}</h3>
                    <p>Scheduled Time: {new Date(meeting.scheduled_time).toLocaleString()}</p>
                    <p>Location: {meeting.location}</p>
                    <NavLink to={`/meetings/${meeting.id}`}>
                        <button id={meeting.id}>More Info</button>
                    </NavLink>
                    <button onClick={handleEdit}>Edit</button>
                    <button onClick={handleDelete}>Delete</button>
                </div>
            )}
        </div>
    );
}

export default MeetingCard;
