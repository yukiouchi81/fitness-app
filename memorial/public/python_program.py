import React, { useState, useEffect } from 'react';
import FusionCharts from 'fusioncharts';
import Charts from 'fusioncharts/fusioncharts.charts';
import ReactFusioncharts from 'react-fusioncharts';
import FusionTheme from 'fusioncharts/themes/fusioncharts.theme.candy';
import Papa from 'papaparse';

// Add FusionCharts capabilities
Charts(FusionCharts);
FusionTheme(FusionCharts);

const Crowdmeter = () => {
  const [currentOccupancy, setCurrentOccupancy] = useState(0);

  useEffect(() => {
    const fetchCurrentOccupancy = () => {
      const csvFilePath = `${process.env.PUBLIC_URL}/dataCsv.csv`;
      Papa.parse(csvFilePath, {
        download: true,
        header: true,
        complete: (results) => {
          try {
            const data = results.data[results.data.length - 1]; // Get the latest entry
            if (data && data.current_occupancy) {
              setCurrentOccupancy(data.current_occupancy);
            } else {
              throw new Error('No valid occupancy data found');
            }
          } catch (error) {
            console.error('Error processing CSV:', error);
          }
        },
        error: (error) => {
          console.error('Error loading CSV:', error);
        }
      });
    };

    // Fetch occupancy on component mount
    fetchCurrentOccupancy();

    // Set up an interval to fetch occupancy every 5 seconds
    const intervalId = setInterval(fetchCurrentOccupancy, 5000);

    // Clean up interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  const dataSource = {
    chart: {
      caption: "Current Gym Occupancy",
      subcaption: "Updated every 5 minutes",
      lowerLimit: "0",
      upperLimit: "120",
      showValue: "1",
      numberSuffix: "%",
      theme: "candy"
    },
    colorRange: {
      color: [
        { minvalue: "0", maxvalue: "60", code: "#F2726F" },
        { minvalue: "60", maxvalue: "90", code: "#FFC533" },
        { minvalue: "90", maxvalue: "120", code: "#62B58F" }
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
      dataFormat="JSON"
      dataSource={dataSource}
    />
  );
};

export default Crowdmeter;
