import React from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';
import Login from './Login';
import Employees from './EmployeeCard';
import Meetings from './Meetings';
import Managers from './Managers';
import EmployeeCardList from './EmployeePage';

const Routes = ({ isLoggedIn, handleLogin }) => {
  return (
    <Switch>
      <Route path="/login">
        {isLoggedIn ? <Redirect to="/reviews" /> : <Login handleLogin={handleLogin} />}
      </Route>
      <Route path="/employees">
        {isLoggedIn ? <EmployeeCardList /> : <Redirect to="/login" />}
      </Route>
      <Route path="/meetings">
        {isLoggedIn ? <Meetings /> : <Redirect to="/login" />}
      </Route>
      <Route path="/managers">
        {isLoggedIn ? <Managers /> : <Redirect to="/login" />}
      </Route>
      <Route path="/">
        <Redirect to={isLoggedIn ? "/reviews" : "/login"} />
      </Route>
    </Switch>
  );
};

export default Routes;