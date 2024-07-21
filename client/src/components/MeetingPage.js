import React, { useEffect, useState } from 'react';
import MeetingCard from './MeetingCard';  // Import MeetingCard component

function MeetingPage() {
    const [meetings, setMeetings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [newTopic, setNewTopic] = useState('');
    const [newScheduledTime, setNewScheduledTime] = useState('');
    const [newLocation, setNewLocation] = useState('');

    useEffect(() => {
        fetch('http://localhost:4000/meetings')
            .then(response => response.json())
            .then(data => {
                setMeetings(data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching meetings:', error);
                setError('Failed to fetch meetings.');
                setLoading(false);
            });
    }, []);

    const handleDelete = (id) => {
        fetch(`http://localhost:4000/meetings/${id}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                setMeetings(meetings.filter(meeting => meeting.id !== id));
            } else {
                console.error('Failed to delete meeting');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

    const handleAdd = (e) => {
        e.preventDefault();
        const newMeeting = {
            topic: newTopic,
            scheduled_time: newScheduledTime,
            location: newLocation,
        };

        fetch('http://localhost:4000/meetings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newMeeting),
        })
        .then(response => response.json())
        .then(addedMeeting => {
            setMeetings([...meetings, addedMeeting]);
            setNewTopic('');
            setNewScheduledTime('');
            setNewLocation('');
        })
        .catch(error => {
            console.error('Error adding meeting:', error);
        });
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div>
            <h1>Meetings</h1>
            <form onSubmit={handleAdd}>
                <input
                    type="text"
                    placeholder="Topic"
                    value={newTopic}
                    onChange={(e) => setNewTopic(e.target.value)}
                    required
                />
                <input
                    type="datetime-local"
                    value={newScheduledTime}
                    onChange={(e) => setNewScheduledTime(e.target.value)}
                    required
                />
                <input
                    type="text"
                    placeholder="Location"
                    value={newLocation}
                    onChange={(e) => setNewLocation(e.target.value)}
                    required
                />
                <button type="submit">Add Meeting</button>
            </form>
            <ul>
                {meetings.map(meeting => (
                    <MeetingCard
                        key={meeting.id}
                        meeting={meeting}
                        onDelete={handleDelete}
                        onUpdate={(updatedMeeting) => {
                            setMeetings(meetings.map(meet =>
                                meet.id === updatedMeeting.id ? updatedMeeting : meet
                            ));
                        }}
                    />
                ))}
            </ul>
        </div>
    );
}

export default MeetingPage;
