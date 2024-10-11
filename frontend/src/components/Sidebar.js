import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = () => {
  return (
    <div>
      <h2>Sidebar</h2>
      <ul>
        <li><Link to="/home/home">Home</Link></li>
        <li><Link to="/home/search">Search</Link></li>
        <li><Link to="/home/browse">Browse</Link></li>
      </ul>
    </div>
  );
};

export default Sidebar;
