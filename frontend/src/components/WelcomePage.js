// src/components/Welcome.js
import React from "react";

const Welcome = ({ userName }) => {
  return (
    <div>
      <h1>Welcome, {userName}!</h1>
      <p>You have successfully logged in.</p>
    </div>
  );
};

export default Welcome;