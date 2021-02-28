import React, { useState, useEffect } from 'react';
import MapView from './components/Map/MapView.js'

import './App.css';

function App() {
  const [obsData, setObsData] = useState([])

  const getObs10 = () => {
    fetch('/obs')
      .then(response => response.json())
      .then(data => {
        console.log(data);
        setObsData(data);
      });
  }

  useEffect(() =>{
    getObs10();
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <MapView
          obsData={obsData}
        />
      </header>
    </div>
  );
}

export default App;
