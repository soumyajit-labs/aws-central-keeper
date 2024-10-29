import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Secrets from './pages/Secrets'
import Login from './pages/Login'
import ProtectedRoute from './components/ProtectedRoute'

function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={ <Login /> } />
        <Route path="/login" element={<Login />} />
        <Route path="/secrets" element={ <ProtectedRoute> <Secrets /> </ProtectedRoute>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
