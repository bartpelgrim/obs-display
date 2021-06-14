import Snackbar from '@material-ui/core/Snackbar'
import MuiAlert from '@material-ui/lab/Alert';

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

export function ErrorSnackbar (props) {
  const { error, setError } = props;

  const onClose = () => {
    setError(null);
  }

  if (error) {
    return (
      <Snackbar
        open={!!error}
        autoHideDuration={5000}
        onClose={onClose}
      >
        <Alert
          severity="error"
          onClose={onClose}
        >
          {error}
        </Alert>
      </Snackbar>
    );
  }
  else {
    return <div/>
  }
}
