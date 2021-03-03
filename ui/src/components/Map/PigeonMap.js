import { Map } from 'pigeon-maps'
import { useState, useEffect } from 'react'

import { PigeonMarker } from './PigeonMarker.js'

function mapTilerProvider(x, y, z) {
  return `https://c.tile.openstreetmap.org/${z}/${x}/${y}.png`
}

const PigeonMap = (props) => {
  const { observations, element } = props;
  const [center, setCenter] = useState([52.3, 5.2]);
  const [zoom, setZoom] = useState(8);
  const [markers, setMarkers] = useState(null);

  useEffect(() => {
    if (observations) {
      const newMarkers = observations.map((obs) => {
        if (obs[element.key]) {
          return (
            <PigeonMarker key={obs.name} anchor={[obs.lat, obs.lon]}>
              {obs[element.key]}
            </PigeonMarker>
          )
        }
      });
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
      {element.displayValue}
    </Map>
  );
};

export default PigeonMap;
