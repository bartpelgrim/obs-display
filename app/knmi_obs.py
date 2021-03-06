from datetime import datetime, timedelta

import requests

from app.exception import ApiException


class KnmiApi:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def _get_latest_file(self) -> str:
        dt = datetime.utcnow() - timedelta(hours=1)
        dt_string = dt.strftime("%Y%m%d%H%M")
        response = requests.get(
            url=f'https://api.dataplatform.knmi.nl/open-data/datasets/Actuele10mindataKNMIstations/versions/2/files',
            headers={
                "Authorization": self.api_key
            },
            params={
                'startAfterFilename': f'KMDS__OPER_P___10M_OBS_L2_{dt_string}'
            },
        )
        if response.status_code == 200:
            files = response.json().get('files')
            if files:
                return files[-1]['filename']
            else:
                raise ApiException('No files available')
        else:
            raise ApiException(f'Unable to get latest files: {response.text}')

    def _get_file_url(self, filename: str) -> str:
        response = requests.get(
            url=f'https://api.dataplatform.knmi.nl/open-data/datasets/Actuele10mindataKNMIstations/versions/2/files/'
                f'{filename}/url',
            headers={
                "Authorization": self.api_key
            },
        )

        if response.status_code == 200:
            return response.json().get('temporaryDownloadUrl')
        else:
            raise ApiException(f'Unable to get file url: {response.text}')

    @staticmethod
    def _get_obs_file(file_url: str) -> bytes:
        response = requests.get(file_url)
        if response.status_code == 200:
            return response.content
        else:
            raise ApiException(f'Unable to get observation file: {response.text}')

    def get_latest_obs(self) -> bytes:
        latest_file = self._get_latest_file()
        file_url = self._get_file_url(latest_file)
        file_content = self._get_obs_file(file_url)

        return file_content
