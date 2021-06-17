import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Label } from 'recharts';
import moment from 'moment'


export default function Graph(props) {
  const { series, element, unit } = props;

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
              interval={0}

              scale={"time"}
            >
              <Label
                  value={"Time"}
                  position={"insideBottom"}
              />
            </XAxis>
            <YAxis
                type={"number"}
                unit={unit}
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
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  }
  else {
    return <div/>
  }
}
