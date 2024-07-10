import React from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';
import Login from './Login';
import Employees from './Employees';
import Reviews from './Reviews';
import Projects from './Projects';
import Managers from './Managers';

const Routes = ({ isLoggedIn, handleLogin }) => {
  return (
    <Switch>
      <Route path="/login">
        {isLoggedIn ? <Redirect to="/reviews" /> : <Login handleLogin={handleLogin} />}
      </Route>
      <Route path="/employees">
        {isLoggedIn ? <Employees /> : <Redirect to="/login" />}
      </Route>
      <Route path="/reviews">
        {isLoggedIn ? <Reviews /> : <Redirect to="/login" />}
      </Route>
      <Route path="/projects">
        {isLoggedIn ? <Projects /> : <Redirect to="/login" />}
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