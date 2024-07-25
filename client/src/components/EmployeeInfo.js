import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import MeetingForm from './MeetingForm'; // Adjust the path as necessary

const EmployeeInfo = () => {
  const params = useParams();
  const [employee, setEmployee] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:4000/employees/${params.id}`)
      .then(res => res.json())
      .then(activeEmployee => setEmployee(activeEmployee));
  }, [params.id]);

  const handleSave = (updatedEmployee) => {
    setEmployee(updatedEmployee);
  };

  return (
    <div>
      {employee ? (
        <div>
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
              employeeId={params.id}
              onSave={handleSave}
            />
          ))}
        </div>
      ) : (
        <div>Employee not found</div>
      )}
    </div>
  );
};

export default EmployeeInfo;

