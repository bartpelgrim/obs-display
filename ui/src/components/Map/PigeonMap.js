import { Map } from 'pigeon-maps'
import { useState, useEffect } from 'react'

import { PigeonMarker } from './PigeonMarker.js'
import WindMarker from '../WindMarker/WindMarker.js'

function mapTilerProvider(x, y, z) {
  return `https://c.tile.openstreetmap.org/${z}/${x}/${y}.png`
}

const PigeonMap = (props) => {
  const { observations, element, dateTime, onMarkerClick } = props;
  const [center, setCenter] = useState([52.3, 5.2]);
  const [zoom, setZoom] = useState(8);
  const [markers, setMarkers] = useState(null);

  useEffect(() => {
    if (observations) {
      const newMarkers = observations.map((obs) => {
        if (obs[element.key] != null) {
          if (element.key === 'wind_direction') {
            return (
              <WindMarker
                key={obs.station.name}
                anchor={[obs.station.latitude, obs.station.longitude]}
                windDirection={obs[element.key]}
                windSpeed={obs["wind_speed_bft"]}
                onMarkerClick={onMarkerClick}
                station={obs.station}
              >
              </WindMarker>
            );
          }
          else {
            return (
              <PigeonMarker
                key={obs.station.name}
                anchor={[obs.station.latitude, obs.station.longitude]}
                value={obs[element.key]}
                element={element}
                onMarkerClick={onMarkerClick}
                station={obs.station}
              />
            );
          }
        }
      });
      setMarkers(newMarkers);
    }
  }, [observations, dateTime, element]);

  return (
    <Map
      height={"90vh"}
      provider={mapTilerProvider}
      center={center}
      zoom={zoom}
      onBoundsChanged={({ center, zoom }) => { setCenter(center); setZoom(zoom) }}
    >
      {markers}
      {element.displayValue} {dateTime?.toLocaleString() ?? ""}
    </Map>
  );
};

export default PigeonMap;
