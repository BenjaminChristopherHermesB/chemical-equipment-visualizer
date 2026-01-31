import './SummaryStats.css';

function SummaryStats({ stats, rowCount }) {
    if (!stats) {
        return <div className="no-data">No statistics available</div>;
    }

    return (
        <div className="summary-stats">
            <h3>Summary Statistics</h3>

            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-label">Total Records</div>
                    <div className="stat-value">{stats.total_count || rowCount || 0}</div>
                </div>

                <div className="stat-card flowrate">
                    <div className="stat-header">Flowrate Statistics</div>
                    <div className="stat-details">
                        <div className="stat-row">
                            <span>Mean:</span>
                            <span>{stats.flowrate?.mean || 0}</span>
                        </div>
                        <div className="stat-row">
                            <span>Min:</span>
                            <span>{stats.flowrate?.min || 0}</span>
                        </div>
                        <div className="stat-row">
                            <span>Max:</span>
                            <span>{stats.flowrate?.max || 0}</span>
                        </div>
                        <div className="stat-row">
                            <span>Std Dev:</span>
                            <span>{stats.flowrate?.std || 0}</span>
                        </div>
                    </div>
                </div>

                <div className="stat-card pressure">
                    <div className="stat-header">Pressure Statistics</div>
                    <div className="stat-details">
                        <div className="stat-row">
                            <span>Mean:</span>
                            <span>{stats.pressure?.mean || 0}</span>
                        </div>
                        <div className="stat-row">
                            <span>Min:</span>
                            <span>{stats.pressure?.min || 0}</span>
                        </div>
                        <div className="stat-row">
                            <span>Max:</span>
                            <span>{stats.pressure?.max || 0}</span>
                        </div>
                        <div className="stat-row">
                            <span>Std Dev:</span>
                            <span>{stats.pressure?.std || 0}</span>
                        </div>
                    </div>
                </div>

                <div className="stat-card temperature">
                    <div className="stat-header">Temperature Statistics</div>
                    <div className="stat-details">
                        <div className="stat-row">
                            <span>Mean:</span>
                            <span>{stats.temperature?.mean || 0}</span>
                        </div>
                        <div className="stat-row">
                            <span>Min:</span>
                            <span>{stats.temperature?.min || 0}</span>
                        </div>
                        <div className="stat-row">
                            <span>Max:</span>
                            <span>{stats.temperature?.max || 0}</span>
                        </div>
                        <div className="stat-row">
                            <span>Std Dev:</span>
                            <span>{stats.temperature?.std || 0}</span>
                        </div>
                    </div>
                </div>

                <div className="stat-card equipment-types">
                    <div className="stat-header">Equipment Types</div>
                    <div className="stat-details">
                        {Object.entries(stats.equipment_types || {}).map(([type, count]) => (
                            <div key={type} className="stat-row">
                                <span>{type}:</span>
                                <span>{count}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default SummaryStats;
