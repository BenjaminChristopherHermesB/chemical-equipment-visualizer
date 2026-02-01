import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    ArcElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar, Line, Doughnut } from 'react-chartjs-2';
import './Charts.css';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    ArcElement,
    Title,
    Tooltip,
    Legend
);

function Charts({ data, summary }) {
    if (!data || data.length === 0) {
        return <div className="no-data">No data available for visualization</div>;
    }

    const flowrateData = {
        labels: data.map((row, idx) => row['Equipment Name'] || `Equipment ${idx + 1}`),
        datasets: [
            {
                label: 'Flowrate',
                data: data.map(row => row.Flowrate || 0),
                backgroundColor: 'rgba(16, 185, 129, 0.6)',
                borderColor: 'rgba(16, 185, 129, 1)',
                borderWidth: 2,
            },
        ],
    };

    const pressureData = {
        labels: data.map((row, idx) => row['Equipment Name'] || `Equipment ${idx + 1}`),
        datasets: [
            {
                label: 'Pressure',
                data: data.map(row => row.Pressure || 0),
                borderColor: 'rgba(245, 158, 11, 1)',
                backgroundColor: 'rgba(245, 158, 11, 0.2)',
                borderWidth: 2,
                tension: 0.4,
            },
        ],
    };

    const temperatureData = {
        labels: data.map((row, idx) => row['Equipment Name'] || `Equipment ${idx + 1}`),
        datasets: [
            {
                label: 'Temperature',
                data: data.map(row => row.Temperature || 0),
                borderColor: 'rgba(239, 68, 68, 1)',
                backgroundColor: 'rgba(239, 68, 68, 0.2)',
                borderWidth: 2,
                tension: 0.4,
            },
        ],
    };

    const equipmentTypes = summary?.equipment_types || {};
    const typeDistributionData = {
        labels: Object.keys(equipmentTypes),
        datasets: [
            {
                label: 'Equipment Type Distribution',
                data: Object.values(equipmentTypes),
                backgroundColor: [
                    'rgba(139, 92, 246, 0.8)',
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(236, 72, 153, 0.8)',
                ],
                borderColor: [
                    'rgba(139, 92, 246, 1)',
                    'rgba(59, 130, 246, 1)',
                    'rgba(16, 185, 129, 1)',
                    'rgba(245, 158, 11, 1)',
                    'rgba(239, 68, 68, 1)',
                    'rgba(236, 72, 153, 1)',
                ],
                borderWidth: 2,
            },
        ],
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            },
        },
    };

    return (
        <div className="charts-container">
            <h2>Data Visualizations</h2>

            <div className="chart-grid">
                <div className="chart-card">
                    <h3>Flowrate Distribution</h3>
                    <div className="chart-container">
                        <Bar data={flowrateData} options={chartOptions} />
                    </div>
                </div>

                <div className="chart-card">
                    <h3>Pressure Trend</h3>
                    <div className="chart-container">
                        <Line data={pressureData} options={chartOptions} />
                    </div>
                </div>

                <div className="chart-card">
                    <h3>Temperature Trend</h3>
                    <div className="chart-container">
                        <Line data={temperatureData} options={chartOptions} />
                    </div>
                </div>

                <div className="chart-card">
                    <h3>Equipment Type Distribution</h3>
                    <div className="chart-container">
                        <Doughnut data={typeDistributionData} options={chartOptions} />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Charts;
