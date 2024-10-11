// UserPage.js
import React from 'react';
import Header from './Header'; // Assume you have a Header component
import Sidebar from './Sidebar'; // Assume you have a Sidebar component
import MainContent from './MainContent'; // Assume you have a MainContent component


const UserPage = () => {
  const username = sessionStorage.getItem('username')

  return (
    <div className='container'>
      <div className='header'>
        <Header/>
      </div>
      <div className='main'>
        <div className="sidebar">
          <Sidebar />
        </div>
        <div className="content">
          <MainContent />
        </div>
      </div>
    </div>
  );
};

export default UserPage;
