import React, { useState } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import Markers from './StationMarkers';


export default function MapView(props) {
  const { obsData } = props;
  const [currentLocation, setCurrentLocation] = useState({ lat: 52.5, lng: 6.0 });
  const [zoom, setZoom] = useState(8);

  return (
    <MapContainer center={currentLocation} zoom={zoom} height={"100vh"}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
      />
      <Markers stations={obsData.observations}/>
    </MapContainer>
  );
}
