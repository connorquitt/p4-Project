


import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import MeetingCard from './MeetingCard';
import '../index.css'; // Adjust the path as necessary

const EmployeeInfo = () => {
  const params = useParams();
  const [employee, setEmployee] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:4000/employees/${params.id}`)
      .then(res => res.json())
      .then(activeEmployee => setEmployee(activeEmployee));
  }, [params.id]);

  function EmployeeMeetings() {
    return employee.meetings.map((meeting) => (
      <div className='employee-meeting' key={meeting.id}>
        <h3>Topic: {meeting.topic}</h3>
        <p>{employee.name} role: </p>
        
        <label>
          Role:
          <input
            type="text"
          />
        </label>
        
        <label>
          RSVP:
          <select>
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
        </label>
      </div>
    ));
  }

  return (
    <div>
      {employee ? (
        <div>
          <h2>{employee.name}</h2>
          <p>Hire Date: {employee.hire_date}</p>
          <p>Manager: {employee.manager.name}</p>
          <p>Department: {employee.manager.department}</p>
          <p>Meetings:</p>
          <EmployeeMeetings />
        </div>
      ) : (
        <div>Employee not found</div>
      )}
    </div>
  );
};

export default EmployeeInfo;
