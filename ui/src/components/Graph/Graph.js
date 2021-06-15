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
              interval={11}

              scale={"time"}
            >
              <Label
                  value={"Time"}
                  position={"insideBottom"}
              />
            </XAxis>
            <YAxis
                typ={"number"}
                unit={unit}
                width={80}
                domain={['dataMin', 'dataMax']}
            >
              <Label
                  value={element.displayValue}
                  position={"insideLeft"}
                  angle={-90}
              />
            </YAxis>
            <Line
                // key={"air_temperature"}
                type={"monotone"}
                dataKey={"air_temperature"}
                stroke={"#ff0000"}
                dot={false}
                strokeOpacity={0.8}
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
