// script.js
const crowdmeterContainer = document.getElementById('crowdmeter');
const crowdmeterLabel = document.getElementById('crowdmeter-label');
const maxOccupancy = 100; // Adjust this value based on your actual maximum occupancy

// Function to render the crowdmeter
function renderCrowdmeter(occupancyData) {
  crowdmeterContainer.innerHTML = '';

  occupancyData.forEach((data, index) => {
    const barHeight = (data.occupancy / maxOccupancy) * 100; // Calculate the bar height as a percentage
    const bar = document.createElement('div');
    bar.classList.add('bar');
    if (index === occupancyData.length - 1) {
      bar.classList.add('current');
      crowdmeterLabel.textContent = `${data.time}: Currently ${getOccupancyLevel(data.occupancy)}`;
    }
    bar.style.height = `${barHeight}%`;
    bar.setAttribute('title', `${data.time}: ${data.occupancy}`);
    crowdmeterContainer.appendChild(bar);

    const label = document.createElement('div');
    label.classList.add('label');
    label.textContent = data.time;
    crowdmeterContainer.appendChild(label);
  });
}

// Function to get the occupancy level based on the occupancy value
function getOccupancyLevel(occupancy) {
  if (occupancy <= 20) {
    return 'not crowded';
  } else if (occupancy <= 50) {
    return 'moderately crowded';
  } else if (occupancy <= 80) {
    return 'crowded';
  } else {
    return 'very crowded';
  }
}

// Function to fetch data from the CSV file
function fetchDataFromCSV() {
  fetch('dataCsv.csv')
    .then(response => response.text())
    .then(data => {
      const occupancyData = [];
      const rows = data.trim().split('\n');
      rows.forEach(row => {
        const [time, occupancy] = row.split(',');
        occupancyData.push({ time, occupancy: parseInt(occupancy, 10) });
      });
      // Render the crowdmeter with the updated occupancyData
      renderCrowdmeter(occupancyData);
    })
    .catch(error => console.error('Error:', error));
}

// Call the fetchDataFromCSV function to display the initial chart
fetchDataFromCSV();

// Update the crowdmeter periodically by fetching data from the CSV file
setInterval(fetchDataFromCSV, 60000); // Update every minute (adjust the interval as needed)