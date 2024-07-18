import React, { useState } from "react";
import '../index.css';
import { NavLink } from "react-router-dom";

function Employees({ employee, onDelete, onUpdate }) {
    const [isEditing, setIsEditing] = useState(false);
    const [newName, setNewName] = useState(employee.name);
    const hireDate = new Date(employee.hire_date).toLocaleDateString(); // Format date

    const handleDelete = () => {
        fetch(`/employees/${employee.id}`, {
            method: 'DELETE'
        })
        .then((response) => {
            if (response.ok) {
                onDelete(employee.id);
            }
        });
    };

    const handleEdit = () => {
        setIsEditing(true);
    };

    const handleSave = () => {
        fetch(`/employees/${employee.id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: newName }),
        })
        .then((response) => response.json())
        .then((updatedEmployee) => {
            onUpdate(updatedEmployee);
            setIsEditing(false);
        });
    };

    return (
        <div key={employee.id} className="card">
            {isEditing ? (
                <div>
                    <input 
                        type="text" 
                        value={newName} 
                        onChange={(e) => setNewName(e.target.value)} 
                    />
                    <button onClick={handleSave}>Save</button>
                </div>
            ) : (
                <div>
                    <h3>Name: {employee.name}</h3>
                    <p>Hire Date: {hireDate}</p>
                    <NavLink to={`/employees/${employee.id}`}>
                        <button id={employee.id}>More Info</button>
                    </NavLink>
                    <button onClick={handleEdit}>Edit</button>
                    <button onClick={handleDelete}>Delete</button>
                </div>
            )}
        </div>
    );
}

export default Employees;


