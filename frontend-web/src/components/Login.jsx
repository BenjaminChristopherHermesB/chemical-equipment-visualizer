import { useState } from 'react';
import { authAPI } from '../services/api';
import './Login.css';

function Login({ onLogin }) {
    const [isRegister, setIsRegister] = useState(false);
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        password2: '',
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            let response;
            if (isRegister) {
                response = await authAPI.register(formData);
            } else {
                response = await authAPI.login({
                    username: formData.username,
                    password: formData.password,
                });
            }

            const { token, user } = response.data;
            onLogin(token, user);
        } catch (err) {
            setError(
                err.response?.data?.error ||
                Object.values(err.response?.data || {}).flat().join(', ') ||
                'An error occurred'
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <h1 className="login-title">Chemical Equipment Visualizer</h1>
                <p className="login-subtitle">
                    {isRegister ? 'Create your account' : 'Sign in to your account'}
                </p>

                {error && <div className="error-message">{error}</div>}

                <form onSubmit={handleSubmit} className="login-form">
                    <div className="form-group">
                        <label>Username</label>
                        <input
                            type="text"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            required
                            disabled={loading}
                        />
                    </div>

                    {isRegister && (
                        <div className="form-group">
                            <label>Email</label>
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                disabled={loading}
                            />
                        </div>
                    )}

                    <div className="form-group">
                        <label>Password</label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            disabled={loading}
                        />
                    </div>

                    {isRegister && (
                        <div className="form-group">
                            <label>Confirm Password</label>
                            <input
                                type="password"
                                name="password2"
                                value={formData.password2}
                                onChange={handleChange}
                                required
                                disabled={loading}
                            />
                        </div>
                    )}

                    <button type="submit" className="primary" disabled={loading}>
                        {loading ? 'Processing...' : isRegister ? 'Register' : 'Login'}
                    </button>
                </form>

                <p className="toggle-form">
                    {isRegister ? 'Already have an account? ' : "Don't have an account? "}
                    <button
                        type="button"
                        onClick={() => {
                            setIsRegister(!isRegister);
                            setError('');
                        }}
                        className="link-button"
                        disabled={loading}
                    >
                        {isRegister ? 'Login' : 'Register'}
                    </button>
                </p>
            </div>
        </div>
    );
}

export default Login;
