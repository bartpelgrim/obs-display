import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';

export function ErrorSnackbar (props) {
  const { error, setError } = props;

  const onClose = () => {
    setError(null);
  }

  if (error) {
    return (
      <Snackbar
        open={!!error}
        anchorOrigin={{vertical: 'bottom', horizontal: 'center'}}
        autoHideDuration={5000}
        onClose={onClose}
      >
        <Alert
          variant='filled'
          severity='error'
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
