import React from "react";
import { Routes, Route } from "react-router-dom";
import DataExplorer from "./DataExplorer";

function Home() {
  return <h1>This is Page 1</h1>;
}

function Search() {
  return <h1>This is Page 2</h1>;
}


function MainContent() {
  return (
    <Routes>
      <Route path="home" element={<Home />} />
      <Route path="search" element={<Search />} />
      <Route path="browse" element={<DataExplorer />} />
      <Route path="/" element={<Home />} /> 
    </Routes>
  );
}

export default MainContent;
