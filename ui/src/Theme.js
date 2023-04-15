import {createTheme} from "@mui/material";

export const theme = createTheme({
  palette: {
    mode: 'dark',
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          textAlign: 'center',
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
        }
      }
    },
    MuiButtonGroup: {
      styleOverrides: {
        root: {
          margin: 5,
        }
      }
    },
    MuiIconButton: {
      defaultProps: {
        color: "primary",
      }
    }
  }
});
