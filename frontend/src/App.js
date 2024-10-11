// App.js
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import LoginForm from './components/LoginForm'; // Your login component
import UserPage from './components/UserPage'; // Your user-specific page
import ProtectedRoute from './components/ProtectedRoute';

const App = () => {

  return (
    <Routes>
    <Route path="/login" element={<LoginForm />} />
    <Route
        path="/home/*"
        element={
        <ProtectedRoute>
            <UserPage />
        </ProtectedRoute>
        }
    />
    <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>

  );
};

export default App;
