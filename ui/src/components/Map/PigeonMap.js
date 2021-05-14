import { Map } from 'pigeon-maps'
import { useState, useEffect } from 'react'

import { PigeonMarker } from './PigeonMarker.js'
import WindMarker from '../WindMarker/WindMarker.js'

function mapTilerProvider(x, y, z) {
  return `https://c.tile.openstreetmap.org/${z}/${x}/${y}.png`
}

const PigeonMap = (props) => {
  const { observations, element, timestamp } = props;
  const [center, setCenter] = useState([52.3, 5.2]);
  const [zoom, setZoom] = useState(8);
  const [markers, setMarkers] = useState(null);
  const [dateTime, setDateTime] = useState(new Date(0));

  useEffect(() => {
    if (observations) {
      const newMarkers = observations.map((obs) => {
        if (obs[element.key] != null) {
          if (element.key === 'wind_direction') {
            return (
              <WindMarker
                key={obs.name}
                anchor={[obs.lat, obs.lon]}
                windDirection={obs[element.key]}
                windSpeed={obs["wind_speed_bft"]}
              >
              </WindMarker>
            );
          }
          else {
            return (
              <PigeonMarker
                key={obs.name}
                anchor={[obs.lat, obs.lon]}
                value={obs[element.key]}
                element={element}
              />
            );
          }
        }
      });
      setDateTime(new Date(timestamp));
      setMarkers(newMarkers);
    }
  }, [observations, element]);

  return (
    <Map
      height={1000}
      provider={mapTilerProvider}
      center={center}
      zoom={zoom}
      onBoundsChanged={({ center, zoom }) => { setCenter(center); setZoom(zoom) }}
    >
      {markers}
      {element.displayValue} {dateTime.toLocaleString()}
    </Map>
  );
};

export default PigeonMap;
