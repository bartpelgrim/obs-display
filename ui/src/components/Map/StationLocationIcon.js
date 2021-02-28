import L from 'leaflet';

// Need to import the marker in order for it to show
import marker from '../../assets/station_location_icon.svg'

export const StationLocationIcon =  L.icon({
  iconUrl: marker,
  iconRetinaUrl: marker,
  iconAnchor: null,
  shadowUrl: null,
  shadowSize: null,
  shadowAnchor: null,
  iconSize: [50, 41],
  className: 'leaflet-venue-icon'
});