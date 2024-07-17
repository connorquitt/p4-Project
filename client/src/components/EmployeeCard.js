import React from "react";
import '../index.css';
import { NavLink } from "react-router-dom";

function Employees({ employee }) {



    return (
        <div key={employee.id} className="card">
            <h3>Name: {employee.name}</h3>
            <p>Hire Date: {employee.hire_date}</p>
            <NavLink to={`/employees/${employee.id}`}><button id={employee.id}>More Info</button></NavLink>
        </div>
    )
}

export default Employees
