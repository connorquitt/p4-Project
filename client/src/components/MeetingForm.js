import React from 'react';
import { useFormik } from 'formik';
import * as yup from 'yup';

const MeetingForm = ({ meeting, meetings, employeeId, onSave }) => {
  const formik = useFormik({
    initialValues: {
      rsvp: meeting.rsvp !== undefined ? meeting.rsvp : "true",
    },
    validationSchema: yup.object({
      rsvp: yup.boolean().required('RSVP is required'),
    }),
    onSubmit: (values) => {
      const updatedMeetings = meetings.map(m => 
        m.id === meeting.id ? { ...m, ...values } : m
      );

      fetch(`http://localhost:4000/employee_meetings/${employeeId}/${meeting.id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rsvp: values.rsvp }),  // Send RSVP value within a dictionary
      })
      .then(async (response) => {
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Error: ${response.statusText}\n${errorText}`);
        }
        return response.json();
      })
      .then((updatedEmployee) => {
        console.log('Updated employee:', updatedEmployee);
        onSave(updatedEmployee);
      })
      .catch((error) => {
        console.error('Error updating employee:', error);
      });
    },
  });

  return (
    <form onSubmit={formik.handleSubmit} >
      <label>
        RSVP:
        <select
          name="rsvp"
          value={formik.values.rsvp.toString()} // Convert boolean to string for select input
          onChange={(e) => formik.setFieldValue('rsvp', e.target.value === 'true')}
          onBlur={formik.handleBlur}
        >
          <option value="true">Yes</option>
          <option value="false">No</option>
        </select>
        {formik.errors.rsvp && formik.touched.rsvp && (
          <p style={{ color: 'red' }}>{formik.errors.rsvp}</p>
        )}
      </label>
      <button type="submit">Save</button>
    </form>
  );
};

export default MeetingForm;

