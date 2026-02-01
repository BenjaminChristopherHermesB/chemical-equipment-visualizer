import { useState } from 'react';
import { useTheme } from '../contexts/ThemeContext';
import { authAPI } from '../services/api';
import './Login.css';

const Login = ({ onLogin }) => {
    const { isDark, toggleTheme } = useTheme();
    const [isRegister, setIsRegister] = useState(false);
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        password2: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            let response;
            if (isRegister) {
                if (formData.password !== formData.password2) {
                    setError('Passwords do not match');
                    setLoading(false);
                    return;
                }
                response = await authAPI.register({
                    username: formData.username,
                    email: formData.email,
                    password: formData.password,
                    password2: formData.password2
                });
            } else {
                response = await authAPI.login({
                    username: formData.username,
                    password: formData.password
                });
            }

            if (response.data && response.data.token) {
                onLogin(response.data.token, response.data.user);
            }
        } catch (err) {
            setError(err.response?.data?.error || err.message || 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-header">
                    <h1 className="login-title">Chemical Equipment Visualizer</h1>
                    <p className="login-subtitle">Analyze and visualize equipment data</p>
                </div>

                <div className="login-tabs">
                    <button
                        className={`tab-button ${!isRegister ? 'active' : ''}`}
                        onClick={() => setIsRegister(false)}
                    >
                        Login
                    </button>
                    <button
                        className={`tab-button ${isRegister ? 'active' : ''}`}
                        onClick={() => setIsRegister(true)}
                    >
                        Register
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="login-form">
                    {error && <div className="error-message">{error}</div>}

                    <div className="input-field">
                        <input
                            type="text"
                            id="username"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            required
                            placeholder=" "
                        />
                        <label htmlFor="username">Username</label>
                    </div>

                    {isRegister && (
                        <div className="input-field">
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                placeholder=" "
                            />
                            <label htmlFor="email">Email (optional)</label>
                        </div>
                    )}

                    <div className="input-field">
                        <input
                            type="password"
                            id="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            placeholder=" "
                        />
                        <label htmlFor="password">Password</label>
                    </div>

                    {isRegister && (
                        <div className="input-field">
                            <input
                                type="password"
                                id="password2"
                                name="password2"
                                value={formData.password2}
                                onChange={handleChange}
                                required
                                placeholder=" "
                            />
                            <label htmlFor="password2">Confirm Password</label>
                        </div>
                    )}

                    <button
                        type="submit"
                        className="submit-button"
                        disabled={loading}
                    >
                        {loading ? 'Please wait...' : (isRegister ? 'Register' : 'Login')}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Login;
