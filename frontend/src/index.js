import React from 'react';
import ReactDOM from 'react-dom/client'; // React 18+
import { BrowserRouter } from 'react-router-dom'; // Import Router
import App from './App'; // Your main App component
import './index.css'; // Global CSS

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);