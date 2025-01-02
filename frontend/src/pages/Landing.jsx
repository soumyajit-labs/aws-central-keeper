import React from 'react';
import '../styles/Landing.css';

const Landing = () => {
    return (
        <div>
            <header className="header">
                <h1>Welcome to Our API Suite</h1>
                <p>Powerful APIs to enhance your applications</p>
            </header>
            <div className="container">
                <section className="intro">
                    <p>
                        Our APIs provide robust, scalable, and easy-to-use solutions for developers looking to integrate essential features into their applications. Explore our documentation and start building today!
                    </p>
                </section>
                <section className="features">
                    <div className="feature">
                        <h3>Authentication API</h3>
                        <p>Secure and reliable authentication for your users.</p>
                    </div>
                    <div className="feature">
                        <h3>Data Analytics API</h3>
                        <p>Powerful tools to analyze and visualize your data.</p>
                    </div>
                    <div className="feature">
                        <h3>Payment API</h3>
                        <p>Seamless and secure payment integration.</p>
                    </div>
                </section>
            </div>
        </div>
    );
};

export default Landing;
