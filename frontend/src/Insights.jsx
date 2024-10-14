import React from 'react';
import { Bar } from 'react-chartjs-2';

const InsightsChart = ({ data }) => {
    const chartData = {
        labels: ['Category 1', 'Category 2', 'Category 3'],
        datasets: [
            {
                label: 'Data Comparison',
                data: data,
                backgroundColor: 'rgba(75,192,192,0.4)',
                borderColor: 'rgba(75,192,192,1)',
            },
        ],
    };

    return (
        <div>
            <Bar data={chartData} />
        </div>
    );
};

export default InsightsChart;
