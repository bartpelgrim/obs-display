import Paper from "@mui/material/Paper";

export default function BasePaper(props) {
  return (
    <Paper sx={{
      textAlign: 'center',
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
    }}>
      {props.children}
    </Paper>
  );
}
