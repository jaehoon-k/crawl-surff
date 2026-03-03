const FareTable = ({ data }) => {
    if (!data || data.length === 0) return null;

    // Sort data reverse chronologically
    const sortedData = [...data].sort((a, b) => {
        return new Date(b.weekStartDate) - new Date(a.weekStartDate);
    });

    return (
        <div className="table-responsive">
            <table className="fare-table">
                <thead>
                    <tr>
                        <th>Year/Week</th>
                        <th>Week Start</th>
                        <th>Week End</th>
                        <th>Ocean Freight (USD)</th>
                    </tr>
                </thead>
                <tbody>
                    {sortedData.map((row, index) => (
                        <tr key={`${row.yearWeek}-${index}`}>
                            <td>{row.yearWeek}</td>
                            <td>{row.weekStartDate || '-'}</td>
                            <td>{row.weekEndDate || '-'}</td>
                            <td className="price-cell">
                                {row.ocf ? `$${row.ocf.toLocaleString()}` : 'N/A'}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default FareTable;
