import React from "react";
import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";

const Layout = () => (
  <div>
    <Navbar />
    <main>
      <Outlet /> {/* This will render the nested routes */}
    </main>
  </div>
);

export default Layout;