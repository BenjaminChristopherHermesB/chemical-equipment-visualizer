import { useState, useEffect } from 'react';
import { datasetAPI, authAPI } from '../services/api';
import CSVUpload from './CSVUpload';
import DataTable from './DataTable';
import Charts from './Charts';
import SummaryStats from './SummaryStats';
import History from './History';
import './Dashboard.css';

function Dashboard({ user, onLogout }) {
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
            <header className="dashboard-header">
                <h1>Chemical Equipment Visualizer</h1>
                <div className="header-right">
                    <span className="user-name">Welcome, {user.username}!</span>
                    <button onClick={handleLogout} className="danger">Logout</button>
                </div>
            </header>

            <div className="dashboard-container">
                <nav className="dashboard-nav">
                    <button
                        className={activeTab === 'upload' ? 'active' : ''}
                        onClick={() => setActiveTab('upload')}
                    >
                        Upload CSV
                    </button>
                    <button
                        className={activeTab === 'visualization' ? 'active' : ''}
                        onClick={() => setActiveTab('visualization')}
                        disabled={!currentDataset}
                    >
                        Visualization
                    </button>
                    <button
                        className={activeTab === 'history' ? 'active' : ''}
                        onClick={() => setActiveTab('history')}
                    >
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
                                <button onClick={handleDownloadPDF} className="primary">
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
