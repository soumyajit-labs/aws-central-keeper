import { OktaAuth } from '@okta/okta-auth-js';
import { Navigate } from "react-router-dom";

const oktaAuth = new OktaAuth({
    issuer: import.meta.env.VITE_OKTA_ISSUER,
    clientId: import.meta.env.VITE_OKTA_CLIENT_ID,
    redirectUri: window.location.origin + '/login/callback',
    scopes: ['openid', 'profile', 'email', 'offline_access']
});

const login = async (username, password) => {
    const signIn = await oktaAuth.signInWithCredentials({
        username: username,
        password: password,
    });
    const { sessionToken } = signIn;
    try {
        const tokens = await oktaAuth.token.getWithoutPrompt({
            responseType: ['token', 'id_token', 'refresh_token'],
            sessionToken: sessionToken,
        });
        oktaAuth.tokenManager.setTokens({
            accessToken: tokens.tokens.accessToken,
            refreshToken: tokens.tokens.refreshToken,
        });
        return tokens.tokens.accessToken.accessToken;
    } catch (error) {
        alert(error)
    }

};

const refreshToken = async () => {
    try {
        const tokenResponse = await oktaAuth.token.renewTokens();
        oktaAuth.tokenManager.setTokens(tokenResponse)
        return tokenResponse.accessToken.accessToken;
    } catch (error) {
        console.error('Error refreshing token', error);
        return <Navigate to="/login" />;
    }
};

export { login, refreshToken };