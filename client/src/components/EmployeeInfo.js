import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import MeetingForm from './MeetingForm'; // Adjust the path as necessary

const EmployeeInfo = () => {
  const params = useParams();
  const [employee, setEmployee] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:4000/employees/${params.id}`)
      .then(res => res.json())
      .then(activeEmployee => {
        if (!activeEmployee.manager) {
          activeEmployee.manager = { name: 'N/A', department: 'N/A' };
        }
        if (!activeEmployee.meetings) {
          activeEmployee.meetings = [];
        }
        console.log('Fetched employee:', activeEmployee);
        setEmployee(activeEmployee);
      });
  }, [params.id]);

  const handleSave = (e) => {
    console.log('Handle save called with:', e.target);
    //setEmployee(updatedEmployee);
  };

  if (!employee) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <div className='card'>
        <h2>{employee.name}</h2>
        <p>Hire Date: {employee.hire_date}</p>
        <p>Manager: {employee.manager.name}</p>
        <p>Department: {employee.manager.department}</p>
        <p>Meetings:</p>
        {employee.meetings.map((meeting) => (
          <MeetingForm
            key={meeting.id}
            meeting={meeting}
            meetings={employee.meetings}
            employeeId={employee.id}
            onSave={handleSave}
          />
        ))}
      </div>
    </div>
  );
};

export default EmployeeInfo;



