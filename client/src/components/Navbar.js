import React from 'react';

const Navbar = ({ setActivePage }) => {
    return (
        <nav>
            <ul>
                <li onClick={() => setActivePage('employees')}>Employees</li>
                <li onClick={() => setActivePage('reviews')}>Reviews</li>
                <li onClick={() => setActivePage('projects')}>Projects</li>
            </ul>
        </nav>
    );
};

export default Navbar;