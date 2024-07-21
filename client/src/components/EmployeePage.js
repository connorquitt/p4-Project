import React, { useEffect, useState } from "react";
import Employees from "./EmployeeCard";

function EmployeeCardList() {
    const [employeeList, setEmployeeList] = useState([]);
    const [name, setName] = useState("");
    const [hireDate, setHireDate] = useState("");
    const [managerId, setManagerId] = useState("");

    useEffect(() => {
        fetch("/employees")
            .then((r) => r.json())
            .then((employees) => setEmployeeList(employees));
    }, []);

    const handleAddEmployee = (e) => {
        e.preventDefault();
        const newEmployee = {
            name: name,
            hire_date: hireDate,
            manager_id: managerId
        };

        fetch("/employees", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newEmployee),
        })
        .then((response) => response.json())
        .then((newEmployee) => {
            setEmployeeList([...employeeList, newEmployee]);
            setName("");
            setHireDate("");
            setManagerId("");
        });
    };

    const handleDeleteEmployee = (id) => {
        fetch(`/employees/${id}`, {
            method: 'DELETE'
        })
        .then((response) => {
            if (response.ok) {
                setEmployeeList(employeeList.filter(employee => employee.id !== id));
            }
        });
    };

    const handleUpdateEmployee = (updatedEmployee) => {
        setEmployeeList(employeeList.map(employee => 
            employee.id === updatedEmployee.id ? updatedEmployee : employee
        ));
    };

    return (
        <div>
            <h1>Employees</h1>
            <form onSubmit={handleAddEmployee}>
                <input
                    type="text"
                    placeholder="Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
                <input
                    type="date"
                    placeholder="Hire Date"
                    value={hireDate}
                    onChange={(e) => setHireDate(e.target.value)}
                    required
                />
                <input
                    type="number"
                    placeholder="Manager ID"
                    value={managerId}
                    onChange={(e) => setManagerId(e.target.value)}
                    required
                />
                <button type="submit">Add Employee</button>
            </form>

            {employeeList.map((employee) => (
                <Employees
                    employee={employee}
                    key={employee.id}
                    onDelete={handleDeleteEmployee}
                    onUpdate={handleUpdateEmployee}
                />
            ))}
        </div>
    );
}

export default EmployeeCardList;
