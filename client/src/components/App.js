import React, { useState, useEffect } from 'react';
import Login from './Login';
import Navbar from './Navbar';
import Employees from './Employees';
import Reviews from './Reviews';
import Projects from './Projects';
import '../index.css';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [activePage, setActivePage] = useState('reviews');

  const handleLogin = (username, password) => {
    //do actual login here omg
    if (username === 'admin' && password === 'password') {
      setIsLoggedIn(true);
    } else {
      alert('Invalid username or password');
    }
  };
  //set this to return http addresses not components
  const renderPage = () => {
    if (!isLoggedIn) {
      return <Login handleLogin={handleLogin} />;
    }

    switch (activePage) {
      case 'employees':
        return <Employees />;
      case 'reviews':
        return <Reviews />;
      case 'projects':
        return <Projects />;
      default:
        return null;
    }
  };

  useEffect(() => {
    fetch("/")
      .then((r) => r.json())
      .then((employees) => console.log(employees));
  }, []);


  return (
    <div className="App">
      <Navbar setActivePage={setActivePage} />
      {renderPage()}
    </div>
  );
};

export default App;