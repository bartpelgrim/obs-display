import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';

export default function ElementMenu(props) {
  const { selectedElement, setSelectedElement, elementConfiguration } = props;

  const onChange = (event) => {
    setSelectedElement(event.target.value);
  };

  return(
    <FormControl size="small" sx={{width: 280, margin: 1}}>
      <Select
        labelId={"element-select-label"}
        id={"element-select-label"}
        value={selectedElement}
        onChange={onChange}
      >
        {elementConfiguration.map((element) =>
          <MenuItem key={element.key} value={element}>{element.displayValue}</MenuItem>
        )}
      </Select>
    </FormControl>
  );
}