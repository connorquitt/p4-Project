import React, { useState } from 'react';
import Login from './Login';
import Navbar from './Navbar';
import Employees from './Employees';
import Reviews from './Reviews';
import Projects from './Projects';
import '../index.css';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [activePage, setActivePage] = useState('employees');

  const handleLogin = (username, password) => {
    //do actual login here omg
    if (username === 'admin' && password === 'password') {
      setIsLoggedIn(true);
    } else {
      alert('Invalid username or password');
    }
  };

  const renderPage = () => {
    if (!isLoggedIn) {
      return <Login handleLogin={handleLogin} />;
    }

    switch (activePage) {
      case 'employees':
        return <Employees />;
      case 'reviews':
        //return <Reviews />;
        return <Login />
      case 'projects':
        return <Projects />;
      default:
        return null;
    }
  };

  return (
    <div className="App">
      <Navbar setActivePage={setActivePage} />
      {renderPage()}
    </div>
  );
};

export default App;