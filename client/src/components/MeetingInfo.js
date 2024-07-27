import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const MeetingInfo = () => {
  const params = useParams()
  const [meeting, setMeeting] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:4000/meetings/${params.id}`)
        .then(res => res.json())
        .then(activeMeeting => setMeeting(activeMeeting))

  }, [params.id]);

  function EmployeesByMeeting() {
    return meeting.employees.map((employee) => (
        <li key={employee}>{employee}</li>
    )

    )
  }


  return (
    <div>
      {meeting ? (
        <div className='card'>
          <h2>{meeting.topic}</h2>
          <p>Scheduled Time: {meeting.scheduled_time}</p>
          <p>Location: {meeting.location}</p>
          <p>Attendees: <EmployeesByMeeting /></p>
        </div>
      ) : (
        <div>Meeting not found</div>
      )}
    </div>
  );
};

export default MeetingInfo;