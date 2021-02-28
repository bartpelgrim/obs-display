import React, { useState, useEffect } from 'react';
import Grid from '@material-ui/core/Grid'
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
        <Grid
          container
          direction={"row"}
          justify={"center"}
          alignItems={"center"}
          display={"flex"}
        >
          <Grid item xs={2}>
            <div>
              <h1>Sidebar</h1>
            </div>
          </Grid>
          <Grid item xs={10}>
            <MapView
              obsData={obsData}
            />
          </Grid>
        </Grid>
      </header>
    </div>
  );
}

export default App;
