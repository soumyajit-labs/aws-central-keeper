import React from 'react';
import '../styles/Navbar.css';
import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav className='navbar'>
            <div className='navbar-left'>
                <Link to="/" className="logo">Integration Accelerator</Link>
            </div>
            <div className='navbar-center'>
                <ul className='nav-links'>
                    <li><Link to="/landing">About APIs</Link></li>
                    <li><Link to="/secrets">Secrets Manager</Link></li>
                </ul>
            </div>
            
        </nav>
    );
};

export default Navbar;