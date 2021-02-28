import React, { Fragment, useState, useEffect } from 'react'
import {Marker} from 'react-leaflet';
import {StationLocationIcon} from './StationLocationIcon';
import MarkerPopup from './MarkerPopup';

const StationMarkers = (props) => {
  const { stations } = props;
  const [markers, setMarkers] = useState(null);

  useEffect(() => {
    if (stations) {
      setMarkers(stations.map((station, index) => (
        <Marker key={index} position={[station.lat, station.lon]} icon={StationLocationIcon} >
          <MarkerPopup data={station}/>
        </Marker>)));
    }
  }, [stations])
  // const markers = stations.map((station, index) => (
  //   <Marker key={index} position={[station.lat, station.lon]} icon={StationLocationIcon} >
  //     <MarkerPopup data={station}/>
  //   </Marker>
  // ));

  if (markers) {
    return <Fragment>{markers}</Fragment>
  }
  else {
    return <div/>
  }
};

export default StationMarkers;