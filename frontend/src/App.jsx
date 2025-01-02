import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Secrets from './pages/Secrets'
import Landing from './pages/Landing'
import ProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route path="/" element={ <ProtectedRoute> <Landing /> </ProtectedRoute>} />
          <Route path="/secrets" element={ <ProtectedRoute> <Secrets /> </ProtectedRoute>} />
          <Route path="/landing" element={ <ProtectedRoute> <Landing /> </ProtectedRoute>} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
