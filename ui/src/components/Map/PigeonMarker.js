import Avatar from '@mui/material/Avatar';
import Tooltip from '@mui/material/Tooltip';


function getFontSize(element, value) {
  const absValue = Math.abs(value);
  if (absValue < 10.0) {
    return 20 - (2 * element.precisionDigits)
  }
  else if (absValue < 100.0) {
    return 20 - (2 * element.precisionDigits)
  }
  else if (absValue < 1000.0) {
    return 18 - (2 * element.precisionDigits)
  }
  else if (absValue < 10000.0) {
    return 16 - (2 * element.precisionDigits)
  }
  else {
    return 14
  }
}

export function PigeonMarker (props) {
  const { left, top, style, onMarkerClick, value, element, children, station } = props;

  const calculateHslValue = (value) => {
    const hslMin = 300;
    const hslMax = -60;
    const lowerBound = element.lowerBound ?? -20;
    const upperBound = element.upperBound ?? 40;

    let hslValue;
    if (value < lowerBound) {
      hslValue = hslMin;
    }
    else if (value > upperBound) {
      hslValue = hslMax;
    }
    else {
      const stepSize = 360.0 / (upperBound - lowerBound);
      hslValue = 300-(stepSize*(value - lowerBound));
      hslValue = Math.round(hslValue);
    }

    if (hslValue < 0) {
      hslValue = hslValue + 360;
    }
    return hslValue;
  }

  const onClick = () => {
    onMarkerClick(station);
  }

  return (
    <Tooltip title={station.name}>
      <Avatar
        sx={{
          position: 'absolute',
          left: left - 20,
          top: top - 20,
          width: 40,
          height: 40,
          background: `hsl(${calculateHslValue(value)}, 100%, 50%)`,
          color: 'black',
          fontSize: getFontSize(element, value)
        }}
        onClick={onClick}
      >
        {value.toFixed(element.precisionDigits)}
        {children}
      </Avatar>
    </Tooltip>
  );
}

