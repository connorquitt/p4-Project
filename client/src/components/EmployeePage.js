import React, {useEffect, useState} from "react";
import Employees from "./EmployeeCard";


  function EmployeeCardList() {

    const [employeeList, setEmployeeList] = useState([])

    useEffect(() => {
        fetch("/employees")
          .then((r) => r.json())
          .then((employees) => setEmployeeList(employees));
      }, []);

    return (
      employeeList.map((employee => {
        return <Employees employee={employee} key={employee.id} />
      }))
    )
  }

  export default EmployeeCardList