import {createTheme} from "@mui/material";

export const theme = createTheme({
  palette: {
    mode: 'dark',
  },
  components: {
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
