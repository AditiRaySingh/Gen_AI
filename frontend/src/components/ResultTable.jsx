function ResultTable({ data }) {
  if (!Array.isArray(data) || data.length === 0) {
    return (
      <div className="empty-result">
        No results found.
      </div>
    );
  }

  const columns = Object.keys(data[0]);

  return (
    <div className="result-table-wrapper">
      <table className="result-table">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column}>
                {column.replaceAll("_", " ")}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map((column) => (
                <td key={column}>
                  {typeof row[column] === "number"
                    ? Number(row[column]).toFixed(2)
                    : row[column]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ResultTable;