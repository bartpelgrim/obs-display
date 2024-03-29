import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';

export default function HistoryMenu(props) {
  const { selectedHistory, setSelectedHistory } = props;

  const onChange = (event) => {
    setSelectedHistory(event.target.value);
  };

  const historyOptions = [
    {key: 1, displayValue: "1h"},
    {key: 3, displayValue: "3h"},
    {key: 6, displayValue: "6h"},
    {key: 12, displayValue: "12h"},
    {key: 24, displayValue: "24h"},
    {key: 48, displayValue: "48h"},
  ]

  return(
    <Select
      size="small"
      sx={{width: 80, margin: 1}}
      labelId={"element-select-label"}
      id={"element-select-label"}
      value={selectedHistory}
      onChange={onChange}
    >
      {historyOptions.map((history) =>
        <MenuItem key={history.key} value={history.key}>{history.displayValue}</MenuItem>
      )}
    </Select>
  );
}