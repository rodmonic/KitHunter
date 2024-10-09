import React from "react";
import { Route, Routes, Navigate } from "react-router-dom"; // Use Navigate for redirecting
import LoginForm from "./components/LoginForm";
import WelcomePage from "./components/WelcomePage";
import LeaguesTable from "./components/LeaguesTable"; 
import ProtectedRoute  from "./components/ProtectedRoute";

const App = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginForm/>} />
      <Route 
        path="/welcome" 
        element={
          <ProtectedRoute>
            <WelcomePage />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/leagues" 
        element={
          <ProtectedRoute>
            <LeaguesTable />
          </ProtectedRoute>
        } 
      />
      <Route path="*" element={<Navigate to="/login" replace />} /> {/* Default redirect */}
    </Routes>
  );
};

export default App;