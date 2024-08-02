from unittest import mock

from app.dataset import ObservationWriter

from tests.helpers.mock_data import mock_data


if __name__ == '__main__':
    with mock_data() as mock_dataset:
        with mock.patch('app.knmi_obs.KnmiApi.get_latest_obs', return_value=mock_dataset):
            with mock.patch('app.dataset.OBSERVATION_TTL_DAYS', 9999):
                writer = ObservationWriter()
                writer.run()
