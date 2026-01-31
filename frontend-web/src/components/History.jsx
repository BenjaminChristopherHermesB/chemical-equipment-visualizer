import { useState, useEffect } from 'react';
import { datasetAPI } from '../services/api';
import './History.css';

function History({ onSelectDataset }) {
    const [datasets, setDatasets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            setLoading(true);
            const response = await datasetAPI.getDatasets();
            setDatasets(response.data.results || []);
        } catch (err) {
            setError('Failed to load history');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
            </div>
        );
    }

    if (error) {
        return <div className="error-message">{error}</div>;
    }

    if (datasets.length === 0) {
        return (
            <div className="no-history">
                <p>No datasets uploaded yet</p>
                <p>Upload a CSV file to get started!</p>
            </div>
        );
    }

    return (
        <div className="history">
            <h2>Recent Uploads (Last 5)</h2>
            <p className="history-description">
                Click on any dataset to view its visualizations
            </p>

            <div className="history-list">
                {datasets.map((dataset) => (
                    <div
                        key={dataset.id}
                        className="history-item"
                        onClick={() => onSelectDataset(dataset.id)}
                    >
                        <div className="history-item-header">
                            <h3>{dataset.filename}</h3>
                            <span className="dataset-id">ID: {dataset.id}</span>
                        </div>
                        <div className="history-item-details">
                            <div className="detail-item">
                                <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                                    <line x1="16" y1="2" x2="16" y2="6" />
                                    <line x1="8" y1="2" x2="8" y2="6" />
                                    <line x1="3" y1="10" x2="21" y2="10" />
                                </svg>
                                <span>{new Date(dataset.uploaded_at).toLocaleString()}</span>
                            </div>
                            <div className="detail-item">
                                <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                    <path d="M9 2v4H5a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-4V2" />
                                    <polyline points="9 2 9 6 15 6 15 2" />
                                </svg>
                                <span>{dataset.row_count} records</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default History;
