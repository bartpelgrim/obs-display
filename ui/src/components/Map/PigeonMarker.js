import Tooltip from '@material-ui/core/Tooltip';


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
      <div style={{
        position: 'absolute',
        left: left - 20,
        top: top - 20,
        width: 40,
        height: 40,
        borderTopLeftRadius: '100%',
        borderTopRightRadius: '100%',
        borderBottomLeftRadius: '100%',
        borderBottomRightRadius: '100%',
        background: `hsl(${calculateHslValue(value)}, 100%, 50%)`,
        color: 'black',
        fontSize: 20,
        ...(style || {})
      }} onClick={onClick}>
        {value.toFixed(element.precisionDigits)}
        {children}
      </div>
    </Tooltip>
  );
}

