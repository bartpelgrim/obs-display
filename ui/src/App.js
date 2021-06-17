import React, { useState, useEffect } from 'react';
import Grid from '@material-ui/core/Grid'
import PigeonMap from './components/Map/PigeonMap.js'
import { elementConfiguration } from './model/Elements'
import { ErrorSnackbar } from './components/Alerts/Alert'
import ElementMenu from './components/SelectionMenu/ElementMenu'
import TimeButtonGroup from './components/TimeButtonGrid/TimeButtonGroup'
import CustomDialog from './components/Dialog/Dialog'

import './App.css';

function App() {
  const [obsData, setObsData] = useState([]);
  const [timeseriesData, setTimeseriesData] = useState(null);
  const [timestamp, setTimestamp] = useState(null);
  const [selectedElement, setSelectedElement] = useState(elementConfiguration[1]);
  const [graphOpen, setGraphOpen] = useState(false);
  const [error, setError] = useState(null);

  const getObs10 = (timestamp = 0) => {
    const url = timestamp !== 0 ? `/obs?timestamp=${timestamp}` : '/obs';
    fetch(url)
      .then(response => {
        if (response.ok) {
          return response.json();
        }
        else {
          if (response.status === 404) {
            const date = new Date(timestamp);
            setError(`Timestamp not found: ${date.toLocaleString()}`);
          }
          else {
            setError(response.statusText);
          }
          return null;
        }
      })
      .then(data => {
        if (data) {
          console.log(data);
          setObsData(data);
          setTimestamp(data.timestamp);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }

  const back10Minutes = () => {
    const newTimestamp = timestamp - (10 * 60 * 1000);
    getObs10(newTimestamp);
  }

  const forward10Minutes = () => {
    const newTimestamp = timestamp + (10 * 60 * 1000)
    getObs10(newTimestamp);
  }

  const getLatestObs = () => {
    getObs10();
  }

  useEffect(() =>{
    getObs10();

    const interval = setInterval(() =>{
      getObs10();
    }, 5*60*1000);
    return () => clearInterval(interval);
  }, [])

  const getStationTimeseries = (stationName) => {
    console.log(stationName)
    setGraphOpen(true);
    const url = `/station?name=${stationName}`;
    fetch(url)
      .then(response => {
        if (response.ok) {
          return response.json();
        }
      })
      .then(data => {
        console.log(data);
        setTimeseriesData(data);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  return (
    <Grid className="App">
      <header className="App-header">
        <ErrorSnackbar
          error={error}
          setError={setError}
        />
        <Grid
          container
          direction={"row"}
          justify={"center"}
          alignItems={"center"}
          display={"flex"}
        >
          <Grid item xs={2}>
            <Grid
              container
              direction={"column"}
              justify={"center"}
              alignItems={"center"}
              display={"flex"}
            >
              <Grid item xs={3}>
                <ElementMenu
                  selectedElement={selectedElement}
                  setSelectedElement={setSelectedElement}
                  elementConfiguration={elementConfiguration}
                />
              </Grid>
              <Grid item xs={3}>
                <TimeButtonGroup
                  backButtonAction={back10Minutes}
                  forwardButtonAction={forward10Minutes}
                  latestButtonAction={getLatestObs}
                />
              </Grid>
            </Grid>
          </Grid>
          <Grid item xs={10}>
            <PigeonMap
              observations={obsData.observations}
              element={selectedElement}
              timestamp={obsData.timestamp}
              onMarkerClick={getStationTimeseries}
            />
          </Grid>
        </Grid>
        <CustomDialog
          selectedElement={selectedElement}
          setSelectedElement={setSelectedElement}
          elementConfiguration={elementConfiguration}
          timeseriesData={timeseriesData}
          dialogOpen={graphOpen}
          setDialogOpen={setGraphOpen}
        />
      </header>
    </Grid>
  );
}

export default App;
