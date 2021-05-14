import React, { useState, useEffect } from 'react';
import Grid from '@material-ui/core/Grid'
import PigeonMap from './components/Map/PigeonMap.js'
import { elementConfiguration } from './model/Elements'
import ElementMenu from './components/SelectionMenu/ElementMenu'

import './App.css';

function App() {
  const [obsData, setObsData] = useState([])
  const [selectedElement, setSelectedElement] = useState(elementConfiguration[1])

  const getObs10 = () => {
    fetch('/obs')
      .then(response => {
        if (response.ok) {
          return response.json();
        }
        else {
          throw new Error(response.statusText);
        }
      })
      .then(data => {
        console.log(data);
        setObsData(data);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  useEffect(() =>{
    getObs10();

    const interval = setInterval(() =>{
      getObs10();
    }, 5*60*1000);
    return () => clearInterval(interval);
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
              <ElementMenu
                selectedElement={selectedElement}
                setSelectedElement={setSelectedElement}
                elementConfiguration={elementConfiguration}
              />
            </div>
          </Grid>
          <Grid item xs={10}>
            <PigeonMap
              observations={obsData.observations}
              element={selectedElement}
              timestamp={obsData.timestamp}
            />
          </Grid>
        </Grid>
      </header>
    </div>
  );
}

export default App;
