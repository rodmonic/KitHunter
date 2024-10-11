import React from "react";
import { Routes, Route } from "react-router-dom";

function Home() {
  return <h1>This is Page 1</h1>;
}

function Search() {
  return <h1>This is Page 2</h1>;
}



function Browse() {
  return (
  <div>
    <div class="flex-container">
      <div class="flex-item">Item 1</div>
      <div class="flex-item">Item 2</div>
      <div class="flex-item">Item 3</div>
    </div>
  </div>
  )
}

function MainContent() {
  return (
    <Routes>
      <Route path="home" element={<Home />} />
      <Route path="search" element={<Search />} />
      <Route path="browse" element={<Browse />} />
      <Route path="/" element={<Home />} /> 
    </Routes>
  );
}

export default MainContent;
