// Modified from https://mui.com/material-ui/react-dialog/#customization "Customized Dialogs"

import React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box'
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';

import ElementMenu from '../SelectionMenu/ElementMenu';
import HistoryMenu from '../SelectionMenu/HistoryMenu';
import Graph from '../Graph/Graph';

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  '& .MuiDialogContent-root': {
    padding: theme.spacing(2),
  },
  '& .MuiDialogActions-root': {
    padding: theme.spacing(1),
  },
}));

function BootstrapDialogTitle(props) {
  const { children, onClose, ...other } = props;

  return (
      <DialogTitle sx={{m: 0, p:2}} {...other}>
        {children}
        {onClose ? (
          <IconButton
            aria-label="close"
            onClick={onClose}
            sx={{
              position: 'absolute' ,
              right: 8,
              top: 8,
              color: (theme) => theme.palette.grey[500],
            }}
          >
            <CloseIcon />
          </IconButton>
        ) : null}
      </DialogTitle>
  )
}

export default function CustomDialog(props) {
  const { selectedElement, setSelectedElement, selectedHistory, setSelectedHistory, selectedStation,
    elementConfiguration, timeseriesData, dialogOpen, setDialogOpen,  } = props;

  const handleClose = () => {
    setDialogOpen(false);
  };

  return (
    <div>
      <BootstrapDialog
        onClose={handleClose}
        aria-labelledby="customized-dialog-title"
        open={dialogOpen}
        fullWidth
        maxWidth={'md'}
      >
        <BootstrapDialogTitle id="customized-dialog-title" onClose={handleClose}>
          {selectedStation?.name}
        </BootstrapDialogTitle>
        <Box sx={{margin: 1}}>
          <ElementMenu
            selectedElement={selectedElement}
            setSelectedElement={setSelectedElement}
            elementConfiguration={elementConfiguration}
          />
          <HistoryMenu
            selectedHistory={selectedHistory}
            setSelectedHistory={setSelectedHistory}
          />
        </Box>
        <Graph
          series={timeseriesData?.timeseries}
          element={selectedElement}
        />
      </BootstrapDialog>
    </div>
  );
}
