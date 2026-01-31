import { useState, useRef } from 'react';
import { datasetAPI } from '../services/api';
import './CSVUpload.css';

function CSVUpload({ onUploadSuccess }) {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState('');
    const [dragActive, setDragActive] = useState(false);
    const fileInputRef = useRef(null);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const handleFile = (selectedFile) => {
        if (!selectedFile.name.endsWith('.csv')) {
            setError('Please upload a CSV file');
            return;
        }
        setFile(selectedFile);
        setError('');
    };

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        setError('');

        try {
            const response = await datasetAPI.uploadCSV(file);
            onUploadSuccess(response.data.dataset);
            setFile(null);
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
        } catch (err) {
            setError(
                err.response?.data?.error ||
                'Failed to upload file. Please check the CSV format.'
            );
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="csv-upload">
            <h2>Upload Equipment Data</h2>
            <p className="upload-description">
                Upload a CSV file with columns: Equipment Name, Type, Flowrate, Pressure, Temperature
            </p>

            {error && <div className="error-message">{error}</div>}

            <div
                className={`drop-zone ${dragActive ? 'drag-active' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".csv"
                    onChange={handleChange}
                    style={{ display: 'none' }}
                />

                <div className="drop-zone-content">
                    <svg className="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <p>Drag and drop your CSV file here, or click to browse</p>
                    {file && <p className="selected-file">Selected: {file.name}</p>}
                </div>
            </div>

            {file && (
                <button
                    onClick={handleUpload}
                    disabled={uploading}
                    className="primary upload-button"
                >
                    {uploading ? 'Uploading...' : 'Upload and Process'}
                </button>
            )}
        </div>
    );
}

export default CSVUpload;
