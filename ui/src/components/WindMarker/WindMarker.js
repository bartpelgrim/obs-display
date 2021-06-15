export default function WindMarker(props) {
  const { left, top, style, onMarkerClick, windDirection, windSpeed, children, stationName } = props;

  const onClick = () => {
    onMarkerClick(stationName);
  }

  return (
    <div
      style={{
        position: 'absolute',
        left: left - 25,
        top: top - 25,
        width: 50,
        height: 50,
        fontSize: 30,
        ...(style || {})
      }}
      onClick={onClick}>
      <svg>
        <path
          transform={`rotate(${windDirection - 180}, 25, 25), scale(0.5)`}
          opacity={0.5}
          d="M 41.565531,90.101159 C 41.863773,73.94019 42.37865,36.214524 42.301866,36.149368 42.26013,36.113922 35.814314,38.91324 27.977842,42.370022 20.14137,45.826807 13.693381,48.629444 13.648975,48.598105 13.482394,48.480542 50.577864,1.0556047 50.747015,1.1698905 50.98748,1.3323629 87.828531,48.181474 87.748588,48.223127 87.713638,48.241317 81.953738,45.526212 74.94879,42.189528 67.943846,38.85284 62.115669,36.122825 61.997288,36.122825 c -0.118382,0 -0.21529,3.744833 -0.215353,8.321851 -5.6e-5,4.577016 -0.07723,18.696872 -0.171481,31.37746 L 61.43907,98.877749 H 51.421319 41.403566 Z"
        />
        <text x={40} y={25} fill="black">
          {windSpeed}
        </text>
      </svg>
      {children}
    </div>
  );
}

