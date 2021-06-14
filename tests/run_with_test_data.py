from unittest import mock

import app.main as main

from tests.helpers.mock_data import mock_data


if __name__ == '__main__':
    with mock_data() as mock_dataset:
        with mock.patch('app.knmi_obs.KnmiApi.get_latest_obs', return_value=mock_dataset):
            main.app.run(host='0.0.0.0')
