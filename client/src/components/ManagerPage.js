import React, { useEffect, useState } from 'react';
import ManagerCard from './ManagerCard';  // Import ManagerCard component

function ManagerPage() {
    const [managers, setManagers] = useState([]);

    useEffect(() => {
        // Fetch the list of managers from the API
        fetch('http://localhost:4000/managers')
            .then(response => response.json())
            .then(data => setManagers(data))
            .catch(error => console.error('Error fetching managers:', error));
    }, []);

    const handleDelete = (id) => {
        // Send a DELETE request to the API
        fetch(`http://localhost:4000/managers/${id}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                // Update the state to remove the deleted manager
                setManagers(managers.filter(manager => manager.id !== id));
            } else {
                console.error('Failed to delete manager');
            }
        })
        .catch(error => console.error('Error:', error));
    };

    const handleAdd = (newManager) => {
        // Send a POST request to add a new manager
        fetch('http://localhost:4000/managers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newManager),
        })
        .then(response => response.json())
        .then(addedManager => {
            // Update the state to include the new manager
            setManagers([...managers, addedManager]);
        })
        .catch(error => console.error('Error adding manager:', error));
    };

    return (
        <div>
            <h1>Managers</h1>
            <form onSubmit={(e) => {
                e.preventDefault();
                const newManager = {
                    name: e.target.name.value,
                    position: e.target.position.value,
                };
                handleAdd(newManager);
                e.target.reset(); // Clear the form fields after submission
            }}>
                <input type="text" name="name" placeholder="Name" required />
                <input type="text" name="position" placeholder="Position" required />
                <button type="submit">Add Manager</button>
            </form>
            <ul>
                {managers.map(manager => (
                    <ManagerCard
                        key={manager.id}
                        manager={manager}
                        onDelete={handleDelete}
                    />
                ))}
            </ul>
        </div>
    );
}

export default ManagerPage;

