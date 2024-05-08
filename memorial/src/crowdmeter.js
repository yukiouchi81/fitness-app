import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom';
import FusionCharts from 'fusioncharts';
import Charts from 'fusioncharts/fusioncharts.charts';
import Widgets from 'fusioncharts/fusioncharts.widgets';
import ReactFusioncharts from 'react-fusioncharts';

// Adding the chart and widget types to FusionCharts
Charts(FusionCharts);
Widgets(FusionCharts);

function Crowdmeter() {
    const [currentOccupancy, setCurrentOccupancy] = useState(0);

    useEffect(() => {
        const fetchCurrentOccupancy = async () => {
            try {
                const response = await fetch('http://localhost:5001/current_occupancy');
                if (!response.ok) {
                    throw new Error('Error fetching current occupancy');
                }
                const data = await response.json();
                setCurrentOccupancy(data.current_occupancy);
            } catch (error) {
                console.error('Error fetching current occupancy:', error);
            }
        };

        fetchCurrentOccupancy();
        const intervalId = setInterval(fetchCurrentOccupancy, 5000); // Update every 5 seconds

        return () => clearInterval(intervalId); // Cleanup on unmount
    }, []);

    const dataSource = {
        chart: {
            caption: "Current Occupancy",
            lowerLimit: "0",
            upperLimit: "120",
            theme: "candy",
            showValue: "1"
        },
        colorRange: {
            color: [
                { minValue: "0", maxValue: "60", code: "#F2726F" },
                { minValue: "60", maxValue: "90", code: "#FFC533" },
                { minValue: "90", maxValue: "120", code: "#62B58F" }
            ]
        },
        dials: {
            dial: [
                { value: currentOccupancy }
            ]
        }
    };

    return (
        <ReactFusioncharts
            type="angulargauge"
            width="100%"
            height="300"
            dataFormat="json"
            dataSource={dataSource}
        />
    );
}

// Check if the script is being loaded on a page that has a 'crowdmeter-root' div
const rootElement = document.getElementById('crowdmeter-root');
if (rootElement) {
    ReactDOM.render(<Crowdmeter />, rootElement);
}

export default Crowdmeter; // Optional: Export is useful if importing the component elsewhere
