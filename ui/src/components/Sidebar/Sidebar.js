import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import ElementMenu from "../SelectionMenu/ElementMenu";
import { elementConfiguration } from "../../model/Elements";
import TimeButtonGroup from "../TimeButtonGrid/TimeButtonGroup";
import { TimeOptions } from "../../model/Time";
import React from "react";

export default function Sidebar(props) {
  const { selectedElement, setSelectedElement, dateTime, back10Minutes, forward10Minutes, getLatestObs } = props;

  return (
    <Paper elevation={2} sx={{padding: 2, margin: 2}}>
      <Grid
        container
        direction={"column"}
        justify={"center"}
        alignItems={"center"}
        display={"flex"}
      >
        <Grid item xs={3} sx={{fontSize: '2vh', margin: 3}}>
          Controls
        </Grid>
        <Grid item xs={3}>
          Selected element:
        </Grid>
        <Grid item xs={3}>
          <ElementMenu
            selectedElement={selectedElement}
            setSelectedElement={setSelectedElement}
            elementConfiguration={elementConfiguration}
          />
        </Grid>
        <Grid item xs={3} paddingTop={2}>
          {dateTime?.toLocaleTimeString([], TimeOptions) ?? "No data available"}
        </Grid>
        <Grid item xs={3}>
          <TimeButtonGroup
            backButtonAction={back10Minutes}
            forwardButtonAction={forward10Minutes}
            latestButtonAction={getLatestObs}
          />
        </Grid>
      </Grid>
    </Paper>
  );
}
