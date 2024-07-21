import React from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';
import Login from './Login';
import MeetingPage from './MeetingPage';
import ManagerCardList from './ManagerPage';
import EmployeeCardList from './EmployeePage';

const Routes = ({ isLoggedIn, handleLogin }) => {
  return (
    <Switch>
      <Route path="/login">
        {isLoggedIn ? <Redirect to="/employees" /> : <Login handleLogin={handleLogin} />}
      </Route>
      <Route path="/employees">
        {isLoggedIn ? <EmployeeCardList /> : <Redirect to="/login" />}
      </Route>
      <Route path="/meetings">
        {isLoggedIn ? <MeetingPage /> : <Redirect to="/login" />}
      </Route>
      <Route path="/managers">
        {isLoggedIn ? <ManagerCardList /> : <Redirect to="/login" />}
      </Route>
      <Route path="/">
        <Redirect to={isLoggedIn ? "/employees" : "/login"} />
      </Route>
    </Switch>
  );
};

export default Routes;