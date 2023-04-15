import IconButton from "@mui/material/IconButton";
import ButtonGroup from '@mui/material/ButtonGroup';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import SkipNextIcon from '@mui/icons-material/SkipNext';
import React from 'react';

export default function TimeButtonGroup(props) {
  const { backButtonAction, forwardButtonAction, latestButtonAction } = props;
  return (
    <ButtonGroup variant="contained" color="primary" aria-label="contained primary button group">
      <IconButton onClick={backButtonAction}>
        <NavigateBeforeIcon/>
      </IconButton>
      <IconButton onClick={forwardButtonAction}>
        <NavigateNextIcon/>
      </IconButton>
      <IconButton onClick={latestButtonAction}>
        <SkipNextIcon/>
      </IconButton>
    </ButtonGroup>
  )
}