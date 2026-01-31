import './DataTable.css';

function DataTable({ data }) {
    if (!data || data.length === 0) {
        return <div className="no-data">No data available</div>;
    }

    const columns = Object.keys(data[0]);

    return (
        <div className="data-table-wrapper">
            <h3>Equipment Data</h3>
            <div className="table-container">
                <table className="data-table">
                    <thead>
                        <tr>
                            {columns.map((column) => (
                                <th key={column}>{column}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {data.map((row, idx) => (
                            <tr key={idx}>
                                {columns.map((column) => (
                                    <td key={column}>
                                        {row[column] !== null && row[column] !== undefined
                                            ? row[column]
                                            : '-'}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default DataTable;
