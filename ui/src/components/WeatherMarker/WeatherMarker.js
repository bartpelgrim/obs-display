import Avatar from '@mui/material/Avatar';
import Box from '@mui/material/Box';
import Tooltip from '@mui/material/Tooltip';

export default function WeatherMarker(props) {
  const { left, top, style, onMarkerClick, station, weatherCode, weatherText } = props;

  const onClick = () => {
    onMarkerClick(station);
  }

  const iconExists = (weatherCode) => {
    return [
      0, 1, 2, 3, 10, 12, 20, 21, 22, 23, 24, 25, 26,
      30, 31, 32, 33, 34, 35, 40,
      50, 51, 52, 53, 54, 55, 56, 57, 58,
      60, 61, 62, 63, 64, 65, 66, 67, 68,
      71, 72, 73, 74, 75, 76, 77, 78,
      80, 81, 82, 83, 84, 85, 86, 87, 89,
      90, 91, 92, 93, 94, 95, 96].includes(weatherCode)
  }

  return (
    <Tooltip title={weatherText}>
      <Avatar
        variant="square"
        sx={{
          position: 'absolute',
          left: left - 20,
          top: top - 20,
          bgcolor: 'rgba(180,180,180,0.8)',
          ...(style || {})
        }}
        onClick={onClick}>
        <Box sx={{marginTop: 0.5}}>
          {
            iconExists(weatherCode) ?
              <img height={40} width={40} src={require(`../../assets/weather-icons/${weatherCode}.png`)} alt={weatherText}/>
              :
              <b>{weatherCode}</b>
          }
        </Box>
      </Avatar>
    </Tooltip>
  );
}

