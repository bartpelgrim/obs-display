import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Label } from 'recharts';
import moment from 'moment'


export default function Graph(props) {
  const { series, element } = props;

  const CustomToolTip = ({active, payload, label}) => {
    if (active && payload && payload.length) {
      return (
        <div>
          <p>{moment(payload[0].payload.timestamp).format("HH:mm")}</p>
          <p>{element.displayValue}: {payload[0].value}</p>
        </div>
      );
    }
    return null;
  }

  if (series) {
    return (
      <div>
        <ResponsiveContainer width="70%" height={300}>
          <LineChart
              data={series}
          >
            <XAxis
              type={'number'}
              dataKey={'timestamp'}
              domain = {['auto', 'auto']}
              height={40}
              tickFormatter={(unixTime) => moment(unixTime).format("HH:mm")}
              interval={2}

              scale={"time"}
            >
              <Label
                  value={"Time"}
                  position={"insideBottom"}
              />
            </XAxis>
            <YAxis
                type={"number"}
                unit={element.unit}
                width={80}
                domain={[dataMin => (Math.round(dataMin - 1)), dataMax => (Math.round(dataMax + 1))]}
                interval={"preserveStartEnd"}
            >
              <Label
                  value={element.displayValue}
                  position={"insideLeft"}
                  angle={-90}
              />
            </YAxis>
            <Line
                // key={"air_temperature"}
                type={"linearOpen"}
                dataKey={element.key}
                stroke={"#ff0000"}
                strokeOpacity={0.8}
                isAnimationActive={false}
            >
            </Line>
            <Tooltip content={<CustomToolTip />}/>
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  }
  else {
    return <div/>
  }
}
