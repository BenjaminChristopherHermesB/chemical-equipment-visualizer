import { useState } from 'react';
import { useTheme } from '../contexts/ThemeContext';
import { datasetAPI, authAPI } from '../services/api';
import CSVUpload from './CSVUpload';
import DataTable from './DataTable';
import Charts from './Charts';
import SummaryStats from './SummaryStats';
import History from './History';
import './Dashboard.css';

function Dashboard({ user, onLogout }) {
    const { isDark, toggleTheme } = useTheme();
    const [currentDataset, setCurrentDataset] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [activeTab, setActiveTab] = useState('upload');

    const handleUploadSuccess = (dataset) => {
        setCurrentDataset(dataset);
        setActiveTab('visualization');
    };

    const handleDatasetSelect = async (datasetId) => {
        try {
            setLoading(true);
            const response = await datasetAPI.getDataset(datasetId);
            setCurrentDataset(response.data);
            setActiveTab('visualization');
        } catch (err) {
            setError('Failed to load dataset');
        } finally {
            setLoading(false);
        }
    };

    const handleDownloadPDF = async () => {
        if (!currentDataset) return;

        try {
            const response = await datasetAPI.downloadPDF(currentDataset.id);
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${currentDataset.filename}_report.pdf`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (err) {
            setError('Failed to download PDF');
        }
    };

    const handleLogout = async () => {
        try {
            await authAPI.logout();
        } catch (err) {
            console.error('Logout error:', err);
        } finally {
            onLogout();
        }
    };

    return (
        <div className="dashboard">
            {/* Theme Toggle FAB */}
            <button
                className="theme-toggle-fab"
                onClick={toggleTheme}
                aria-label="Toggle theme"
            >
                {isDark ? (
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41l-1.06-1.06zm1.06-10.96c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z" />
                    </svg>
                ) : (
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z" />
                    </svg>
                )}
            </button>

            <header className="dashboard-header">
                <h1>Chemical Equipment Visualizer</h1>
                <div className="header-right">
                    <span className="user-name">Welcome, {user.username}!</span>
                    <button onClick={handleLogout} className="logout-button">Logout</button>
                </div>
            </header>

            <div className="dashboard-container">
                <nav className="dashboard-nav">
                    <button
                        className={`nav-button ${activeTab === 'upload' ? 'active' : ''}`}
                        onClick={() => setActiveTab('upload')}
                    >
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M9 16h6v-6h4l-7-7-7 7h4v6zm-4 2h14v2H5v-2z" />
                        </svg>
                        Upload CSV
                    </button>
                    <button
                        className={`nav-button ${activeTab === 'visualization' ? 'active' : ''}`}
                        onClick={() => setActiveTab('visualization')}
                        disabled={!currentDataset}
                    >
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z" />
                        </svg>
                        Visualization
                    </button>
                    <button
                        className={`nav-button ${activeTab === 'history' ? 'active' : ''}`}
                        onClick={() => setActiveTab('history')}
                    >
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z" />
                        </svg>
                        History
                    </button>
                </nav>

                <div className="dashboard-content">
                    {error && <div className="error-message">{error}</div>}

                    {activeTab === 'upload' && (
                        <CSVUpload onUploadSuccess={handleUploadSuccess} />
                    )}

                    {activeTab === 'visualization' && currentDataset && (
                        <div className="visualization-container">
                            <div className="dataset-header">
                                <h2>{currentDataset.filename}</h2>
                                <button onClick={handleDownloadPDF} className="pdf-button">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                        <path d="M19 12v7H5v-7H3v7c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-7h-2zm-6 .67l2.59-2.58L17 11.5l-5 5-5-5 1.41-1.41L11 12.67V3h2v9.67z" />
                                    </svg>
                                    Download PDF Report
                                </button>
                            </div>

                            <SummaryStats
                                stats={currentDataset.summary_stats}
                                rowCount={currentDataset.row_count}
                            />

                            <DataTable data={currentDataset.raw_data} />

                            <Charts
                                data={currentDataset.raw_data}
                                summary={currentDataset.summary_stats}
                            />
                        </div>
                    )}

                    {activeTab === 'history' && (
                        <History onSelectDataset={handleDatasetSelect} />
                    )}
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
