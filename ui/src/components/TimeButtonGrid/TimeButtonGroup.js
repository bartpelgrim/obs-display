import { Button, ButtonGroup } from '@material-ui/core'
import React from 'react'

export default function TimeButtonGroup(props) {
  const { backButtonAction, forwardButtonAction, latestButtonAction } = props;
  return (
    <ButtonGroup variant="contained" color="primary" aria-label="contained primary button group">
      <Button onClick={backButtonAction}>{"<"}</Button>
      <Button onClick={forwardButtonAction}>{">"}</Button>
      <Button onClick={latestButtonAction}>{">|"}</Button>
    </ButtonGroup>
  )
}