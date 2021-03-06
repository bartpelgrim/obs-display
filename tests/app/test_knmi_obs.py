# pip
import pytest
import requests_mock

# app
from app.exception import ApiException
from app.knmi_obs import KnmiApi, API_BASE_URL


class TestKnmiApi:
    @pytest.fixture(autouse=True)
    def __around(self):
        self.api = KnmiApi('foo')
        with requests_mock.Mocker() as self.m:
            yield

    def test_get_latest_file(self):
        mock_response_text = '''{
            "maxResults": 10,
            "resultCount": 6,
            "startAfterFilename": "KMDS__OPER_P___10M_OBS_L2_202103060919",
            "files": [
                {
              "filename" : "KMDS__OPER_P___10M_OBS_L2_202103060920.nc",
              "size" : 189174,
              "lastModified" : "2021-03-06T09:56:04+00:00"
            },
                {
              "filename" : "KMDS__OPER_P___10M_OBS_L2_202103060930.nc",
              "size" : 189199,
              "lastModified" : "2021-03-06T10:05:54+00:00"
            },
                {
              "filename" : "KMDS__OPER_P___10M_OBS_L2_202103060940.nc",
              "size" : 189171,
              "lastModified" : "2021-03-06T10:16:27+00:00"
            },
                {
              "filename" : "KMDS__OPER_P___10M_OBS_L2_202103060950.nc",
              "size" : 188981,
              "lastModified" : "2021-03-06T10:16:29+00:00"
            },
                {
              "filename" : "KMDS__OPER_P___10M_OBS_L2_202103061000.nc",
              "size" : 189082,
              "lastModified" : "2021-03-06T10:16:30+00:00"
            },
                {
              "filename" : "KMDS__OPER_P___10M_OBS_L2_202103061010.nc",
              "size" : 189176,
              "lastModified" : "2021-03-06T10:16:33+00:00"
            }
              ],
          "isTruncated": false
        }
        '''
        self.m.get(API_BASE_URL,
                   text=mock_response_text,
                   status_code=200)
        assert self.api._get_latest_file() == 'KMDS__OPER_P___10M_OBS_L2_202103061010.nc'

    def test_get_latest_file_raises_exception_when_file_list_empty(self):
        mock_response_text = '''{
            "maxResults": 10,
            "resultCount": 6,
            "startAfterFilename": "KMDS__OPER_P___10M_OBS_L2_202103060919",
            "files": [],
          "isTruncated": false
        }
        '''
        self.m.get(API_BASE_URL,
                   text=mock_response_text,
                   status_code=200)
        with pytest.raises(ApiException):
            self.api._get_latest_file()

    def test_get_latest_file_raises_exception_when_request_fails(self):
        mock_response_text = '''
            {
                "error": "Access to this resource has been disallowed"
            }
        '''
        self.m.get(API_BASE_URL,
                   text=mock_response_text,
                   status_code=403)
        with pytest.raises(ApiException):
            self.api._get_latest_file()
