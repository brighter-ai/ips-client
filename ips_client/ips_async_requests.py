import httpx
import logging
import urllib.parse

from typing import Dict, Optional, IO
from uuid import UUID

from ips_client.data_models import ServiceType, OutputType, JobArguments
from ips_client.utils import normalize_url
from ips_client.settings import Settings


settings = Settings()

logging.basicConfig(level=settings.log_level)
log = logging.getLogger('ips-requests')


class IPSAsyncRequests:
    """
    Helper class wrapping requests to the IPS API.
    """

    API_VERSION = 'v3'

    def __init__(self, ips_url: str = settings.ips_url_default):
        self.ips_url = normalize_url(ips_url)

    async def post_job(self, file: IO, service: ServiceType, out_type: OutputType,
                       job_args: JobArguments = JobArguments(), file_name: Optional[str] = None) -> Dict:
        """
        Post the job via a post request.
        """

        # We need a file name with extension.
        # For file streams opened from disk, the name is available.
        # But for other streams it is not.
        if not file_name:
            try:
                file_name = file.name
            except AttributeError:
                raise ValueError('Please specify file_name (including extension)!')

        files = {'file': (file_name, file)}

        url = urllib.parse.urljoin(self.ips_url, f'/{service}/{self.API_VERSION}/{out_type}')

        query_args = {k: str(v) for k, v in job_args.dict(exclude_none=True).items()}

        async with httpx.AsyncClient() as client:
            response = await client.post(url=url,
                                         files=files,
                                         params=query_args)

        if response.status_code != 200:
            raise RuntimeError(f'Error while posting job: {response}')

        return response.json()

    async def get_output(self, service: ServiceType, out_type: OutputType, output_id: UUID) -> bytes:

        url = urllib.parse.urljoin(self.ips_url, f'/{service}/{self.API_VERSION}/{out_type}/{output_id}')

        with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=settings.requests_timeout)

        if response.status_code != 200:
            raise RuntimeError(f'Error while getting job result: {response}')

        return response.content

    async def get_status(self, service: ServiceType, out_type: OutputType, output_id: UUID) -> Dict:

        url = urllib.parse.urljoin(self.ips_url, f'/{service}/{self.API_VERSION}/{out_type}/{output_id}/status')

        with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=settings.requests_timeout)

        if response.status_code != 200:
            raise RuntimeError(f'Error while getting job status: {response}')

        return response.json()

    async def delete_output(self, service: ServiceType, out_type: OutputType, output_id: UUID) -> Dict:

        url = urllib.parse.urljoin(self.ips_url, f'/{service}/{self.API_VERSION}/{out_type}/{output_id}')

        with httpx.AsyncClient() as client:
            response = await client.delete(url, timeout=settings.requests_timeout)

        if response.status_code != 200:
            raise RuntimeError(f'Error while deleting job: {response}')

        return response.json()

    async def get_error(self, service: ServiceType, out_type: OutputType, output_id: UUID) -> Dict:

        url = urllib.parse.urljoin(self.ips_url, f'/{service}/{self.API_VERSION}/{out_type}/{output_id}/error')

        with httpx.AsyncClient() as client:
            response = client.get(url, timeout=settings.requests_timeout)

        if response.status_code != 200:
            raise RuntimeError(f'Error while getting job error: {response}')

        return response.json()