// ProtectedRoute.js
import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const token = sessionStorage.getItem('token'); // Check for token

  // If no token, redirect to login
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // If token exists, render the children components
  return children;
};

export default ProtectedRoute;
