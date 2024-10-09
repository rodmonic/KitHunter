import React from "react";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  const token = sessionStorage.getItem("token"); // Check if the token exists

  if (!token) {
    // If not authenticated, redirect to the login page
    return <Navigate to="/login" replace />;
  }

  return children; // If authenticated, render the children components
};

export default ProtectedRoute;