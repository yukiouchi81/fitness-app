import React, { useEffect, useState } from 'react';
import FusionCharts from 'fusioncharts';
import Charts from 'fusioncharts/fusioncharts.charts';
import ReactFC from 'react-fusioncharts';
import Papa from 'papaparse';

// Enable FusionCharts in React
ReactFC.fcRoot(FusionCharts, Charts);

const OccupancyChart = () => {
    const [currentOccupancy, setCurrentOccupancy] = useState(null);
    const [error, setError] = useState('');

    const fetchCurrentOccupancy = () => {
        // Using a relative URL to access the CSV file in the public directory
        const csvFilePath = process.env.PUBLIC_URL + '/dataCsv.csv';

        Papa.parse(csvFilePath, {
            download: true,
            header: true, // Assuming the CSV has headers; adjust if not
            complete: (results) => {
                try {
                    const data = results.data[0]; // Assuming the relevant data is in the first row
                    if (data.current_occupancy) {
                        setCurrentOccupancy(data.current_occupancy);
                    } else {
                        throw new Error('No occupancy data found');
                    }
                } catch (error) {
                    console.error('Error processing CSV:', error);
                    setError('Failed to process occupancy data.');
                }
            },
            error: (error) => {
                console.error('Error loading CSV:', error);
                setError('Failed to load occupancy data.');
            }
        });
    };

    useEffect(() => {
        fetchCurrentOccupancy();
        const intervalId = setInterval(fetchCurrentOccupancy, 5000); // Update every 5 seconds

        // Clean up
        return () => clearInterval(intervalId);
    }, []);

    const chartConfigs = {
        type: 'angulargauge',
        width: '100%',
        height: '300',
        dataFormat: 'json',
        dataSource: {
            chart: {
                caption: 'Current Occupancy',
                lowerLimit: '0',
                upperLimit: '120',
                theme: 'candy',
                showValue: '1'
            },
            colorRange: {
                color: [
                    { minValue: '0', maxValue: '60', code: '#F2726F' },
                    { minValue: '60', maxValue: '90', code: '#FFC533' },
                    { minValue: '90', maxValue: '120', code: '#62B58F' }
                ]
            },
            dials: { dial: [{ value: currentOccupancy || '0' }] }
        }
    };

    return (
        <div>
            {error ? <p>{error}</p> : <ReactFC {...chartConfigs} />}
        </div>
    );
};

export default OccupancyChart;
