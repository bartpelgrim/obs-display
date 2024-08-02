import { LineChart } from '@mui/x-charts/LineChart';
import moment from 'moment';


export default function Graph(props) {
  const { series, element } = props;


  if (series) {
    return (
      <LineChart
        dataset={series}
        xAxis={[
          {
            dataKey: 'timestamp',
            scaleType: 'time',
            label: 'Time',
            valueFormatter: (timestamp, context) => moment(timestamp).format("HH:mm"),
          }
          ]}
        yAxis={[
          {
            label: `${element.displayValue} (${element.unit ?? "-"})`,
          }
        ]}
        series={[
          {
            dataKey: element.key,
            label: element.displayValue,
            valueFormatter: (v) => `${v} ${element.unit ?? "-"}`,
            color: '#e15759',
            showMark: series.length < 50,
            curve: 'linear',
          }
        ]}
        grid={{vertical: true, horizontal: true}}
        height={500}
        margin={{
          left: 80,
          right: 50,
          top: 50,
          bottom: 80,
        }}
        skipAnimation={true}
        // Move label of Y-Axis to the left
        sx={{['.MuiChartsAxis-directionY .MuiChartsAxis-label']: {transform: 'translateX(-25px)'}}}
      />
    );
  }
  else {
    return <div/>
  }
}
