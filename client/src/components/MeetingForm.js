import React, { useState } from 'react';
import { useFormik } from 'formik';
import * as yup from 'yup';

const MeetingForm = ({ meeting, meetings, employeeId, onSave }) => {
  const [isEditing, setIsEditing] = useState(false);

  const formik = useFormik({
    initialValues: {
      role: meeting.role,
      rsvp: meeting.rsvp,
    },
    validationSchema: yup.object({
      role: yup.string().required('Role is required').max(50, 'Role must be 50 characters or less'),
      rsvp: yup.string().oneOf(['yes', 'no'], 'Invalid RSVP')
    }),
    onSubmit: (values) => {
      const updatedMeetings = meetings.map(m => 
        m.id === meeting.id ? { ...m, ...values } : m
      );

      fetch(`http://localhost:4000/employee_meetings/${employeeId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ meetings: updatedMeetings }),
      })
      .then(async (response) => {
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Error: ${response.statusText}\n${errorText}`);
        }
        return response.json();
      })
      .then((updatedEmployee) => {
        onSave(updatedEmployee);
        setIsEditing(false);
      })
      .catch((error) => {
        console.error('Error updating employee:', error);
      });
    },
  });

  return (
    <div className='employee-meeting'>
      <h3>Topic: {meeting.topic}</h3>
      {isEditing ? (
        <form onSubmit={formik.handleSubmit}>
          <label>
            Role:
            <input
              type="text"
              name="role"
              value={formik.values.role}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              placeholder="Role"
            />
            {formik.errors.role && formik.touched.role && (
              <p style={{ color: 'red' }}>{formik.errors.role}</p>
            )}
          </label>
          <label>
            RSVP:
            <select
              name="rsvp"
              value={formik.values.rsvp}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
            >
              <option value="yes">Yes</option>
              <option value="no">No</option>
            </select>
            {formik.errors.rsvp && formik.touched.rsvp && (
              <p style={{ color: 'red' }}>{formik.errors.rsvp}</p>
            )}
          </label>
          <button type="submit">Save</button>
          <button type="button" onClick={() => setIsEditing(false)}>Cancel</button>
        </form>
      ) : (
        <div>
          <span>{meeting.role}</span>
          <span>{meeting.rsvp}</span>
          <button onClick={() => setIsEditing(true)}>Edit</button>
        </div>
      )}
    </div>
  );
};

export default MeetingForm;
