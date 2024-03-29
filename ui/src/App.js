import React, { useState, useEffect } from 'react';
import Grid from '@mui/material/Grid';
import BasePaper from "./components/Paper/BasePaper";
import PigeonMap from './components/Map/PigeonMap.js';
import { elementConfiguration } from './model/Elements';
import { ErrorSnackbar } from './components/Alerts/Alert';
import Sidebar from "./components/Sidebar/Sidebar";
import CustomDialog from './components/Dialog/Dialog';

import './App.css';
import {ThemeProvider} from "@mui/material";
import { theme } from "./Theme";

function App() {
  const [obsData, setObsData] = useState([]);
  const [timeseriesData, setTimeseriesData] = useState(null);
  const [timestamp, setTimestamp] = useState(null);
  const [dateTime, setDateTime] = useState(null);
  const [selectedElement, setSelectedElement] = useState(elementConfiguration[1]);
  const [selectedStation, setSelectedStation] = useState(null);
  const [selectedHistory, setSelectedHistory] = useState(3);
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
          setObsData(data.observations);
          setTimestamp(data.timestamp);
          setDateTime(new Date(data.timestamp));
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

  const getStationTimeseries = (station) => {
    const url = `/station?id=${station.id}&historyHours=${selectedHistory}`;
    fetch(url)
      .then(response => {
        if (response.ok) {
          return response.json();
        }
      })
      .then(data => {
        setTimeseriesData(data);
      })
      .catch((error) => {
      });
  }

  useEffect(() => {
    if (selectedStation) {
      getStationTimeseries(selectedStation);
    }
  }, [selectedHistory, selectedStation]);

  const onMarkerClick = (station) => {
    setSelectedStation(station);
    setGraphOpen(true);
  }

  return (
    <ThemeProvider theme={theme}>
      <BasePaper>
        <ErrorSnackbar
          error={error}
          setError={setError}
        />
        <Grid
          container
          alignItems={"center"}
          display={"flex"}
        >
          <Grid item xs md={6} lg={4} xl={3}>
            <Sidebar
              selectedElement={selectedElement}
              setSelectedElement={setSelectedElement}
              dateTime={dateTime}
              back10Minutes={back10Minutes}
              forward10Minutes={forward10Minutes}
              getLatestObs={getLatestObs}
            />
          </Grid>
          <Grid item xs={12} md={12} lg={8} xl={9} sx={{fontSize: '3vh'}}>
            <PigeonMap
              observations={obsData}
              element={selectedElement}
              dateTime={dateTime}
              onMarkerClick={onMarkerClick}
            />
          </Grid>
        </Grid>
        <CustomDialog
          selectedElement={selectedElement}
          setSelectedElement={setSelectedElement}
          selectedHistory={selectedHistory}
          setSelectedHistory={setSelectedHistory}
          elementConfiguration={elementConfiguration}
          selectedStation={selectedStation}
          timeseriesData={timeseriesData}
          dialogOpen={graphOpen}
          setDialogOpen={setGraphOpen}
        />
      </BasePaper>
    </ThemeProvider>
  );
}

export default App;
