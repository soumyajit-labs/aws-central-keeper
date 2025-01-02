import { ACCESS_TOKEN } from "../constants";
import { useState, useEffect } from "react";

function ProtectedRoute({ children }) {
    const [isAuthorized, setIsAuthorized] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const validateCookies = async () => {
            try {
                const response = await axios.get("https://sso-gatekeeper.onrender.com/verify", { withCredentials: true });
                if (response.status === 200 && response.data.valid) {
                    localStorage.setItem(ACCESS_TOKEN, response.data.access_token);
                    setIsAuthorized(true);
                } else {
                    setIsAuthorized(false);
                }
            } catch (error) {
                console.error("Token validation failed:", error);
                setIsAuthorized(false);
            } finally {
                setIsLoading(false);
            }
        };
        validateCookies();
    }, []);
    
    if (isLoading) {
        return <div>Loading...</div>;
    }
    
    if (!isAuthorized) {
        // window.location.href = 'https://dev-63025152.okta.com/';
        return null;
    }

    return <>{children}</>;
}

export default ProtectedRoute;