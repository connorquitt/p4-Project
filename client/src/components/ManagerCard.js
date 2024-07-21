import React from "react";
import '../index.css';

function ManagerCard({ manager, onDelete, onUpdate }) {
    
    if (!manager) {
        return null; // or return a loading state if manager is undefined
    }

    const handleDelete = () => {
        fetch(`/managers/${manager.id}`, {
            method: 'DELETE'
        })
        .then((response) => {
            if (response.ok) {
                onDelete(manager.id);
            }
        });
    };

    return (
        <div key={manager.id} className="card">
                <div>
                    <h3>Name: {manager.name}</h3>
                    <p>Position: {manager.position}</p>
                    <button onClick={handleDelete}>Delete</button>
                </div>
            
        </div>
    );
}

export default ManagerCard;
