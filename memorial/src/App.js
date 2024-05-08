import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Crowdmeter from './crowdmeter';  // Correct path if Crowdmeter.js is in the same directory as App.js

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/crowdmeter" element={<Crowdmeter />} />
                {/* other routes can go here */}
            </Routes>
        </Router>
    );
}

export default App;
