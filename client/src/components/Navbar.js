import React from 'react';
import { NavLink } from 'react-router-dom';
import '../index.css';

function NavBar({ handleLogOut }) {
    return (
        <nav className='navbar'>
            <NavLink to='/employees'>Employees</NavLink>
            <NavLink to='/reviews'>Reviews</NavLink>
            <NavLink to='/projects'>Projects</NavLink>
            <NavLink to='/managers'>Managers</NavLink>
            <NavLink to='/login' onClick={handleLogOut}>Logout</NavLink>
        </nav>
    )
}

export default NavBar;