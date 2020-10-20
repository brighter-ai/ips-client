import requests
import urllib.parse

from io import BufferedIOBase
from typing import Dict
from uuid import UUID

from ips_client.data_models import ServiceType, OutputType, JobArguments
from ips_client.utils import normalize_url


REQUESTS_TIMEOUT = 15


class IPSApiWrapper:

    API_VERSION = 'v3'

    def __init__(self, ips_url: str = 'http://127.0.0.1:8787/'):
        self.ips_url = normalize_url(ips_url)

    def post_job(self, file: BufferedIOBase, service: ServiceType, out_type: OutputType, job_args: JobArguments) -> Dict:
        """
        Post the job via a post request.
        """

        url = urllib.parse.urljoin(self.ips_url, f'/{service}/{self.API_VERSION}/{out_type}')
        files = {'file': file}

        response = requests.post(url=url,
                                 files=files,
                                 params=job_args.dict(),
                                 timeout=REQUESTS_TIMEOUT)

        if response.status_code != 200:
            raise RuntimeError(f'Error while posting job: {response}')

        return response.json()

    def get_output(self, service: ServiceType, out_type: OutputType, output_id: UUID) -> bytes:

        url = urllib.parse.urljoin(self.ips_url, f'/{service}/{self.API_VERSION}/{out_type}/{output_id}')
        response = requests.get(url, timeout=REQUESTS_TIMEOUT)

        if response.status_code != 200:
            raise RuntimeError(f'Error while getting job result: {response}')

        return response.content

    def get_status(self, service: ServiceType, out_type: OutputType, output_id: UUID) -> Dict:

        url = urllib.parse.urljoin(self.ips_url, f'/{service}/{self.API_VERSION}/{out_type}/{output_id}/status')
        response = requests.get(url, timeout=REQUESTS_TIMEOUT)

        if response.status_code != 200:
            raise RuntimeError(f'Error while getting job status: {response}')

        return response.json()

    def delete_output(self, service: ServiceType, out_type: OutputType, output_id: UUID) -> Dict:

        url = urllib.parse.urljoin(self.ips_url, f'/{service}/{self.API_VERSION}/{out_type}/{output_id}')
        response = requests.delete(url, timeout=REQUESTS_TIMEOUT)

        if response.status_code != 200:
            raise RuntimeError(f'Error while deleting job: {response}')

        return response.json()

    def get_error(self, service: ServiceType, out_type: OutputType, output_id: UUID) -> Dict:

        url = urllib.parse.urljoin(self.ips_url, f'/{service}/{self.API_VERSION}/{out_type}/{output_id}/error')
        response = requests.get(url, timeout=REQUESTS_TIMEOUT)

        if response.status_code != 200:
            raise RuntimeError(f'Error while getting job error: {response}')

        return response.json()