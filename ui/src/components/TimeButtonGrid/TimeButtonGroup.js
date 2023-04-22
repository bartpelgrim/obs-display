import React from 'react';
import IconButton from "@mui/material/IconButton";
import ButtonGroup from '@mui/material/ButtonGroup';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import SkipNextIcon from '@mui/icons-material/SkipNext';
import Tooltip from "@mui/material/Tooltip";

export default function TimeButtonGroup(props) {
  const { backButtonAction, forwardButtonAction, latestButtonAction } = props;
  return (
    <ButtonGroup variant="contained" color="primary" aria-label="contained primary button group">
      <IconButton onClick={backButtonAction}>
        <Tooltip title="One step back">
          <NavigateBeforeIcon/>
        </Tooltip>
      </IconButton>
      <IconButton onClick={forwardButtonAction}>
        <Tooltip title="One step forward">
          <NavigateNextIcon/>
        </Tooltip>
      </IconButton>
      <IconButton onClick={latestButtonAction}>
        <Tooltip title="Latest observations">
          <SkipNextIcon/>
        </Tooltip>
      </IconButton>
    </ButtonGroup>
  )
}