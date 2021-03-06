import pytest

from redact.data_models import ServiceType, OutputType
from redact.redact_instance import RedactInstance
from redact.redact_job import RedactJob
from redact.redact_requests import RedactRequests
from redact.settings import Settings


settings = Settings()


@pytest.fixture
def redact_requests(redact_url) -> RedactRequests:
    return RedactRequests(redact_url=redact_url)


@pytest.fixture(params=[ServiceType.dnat, ServiceType.blur, ServiceType.extract])
def any_img_redact_inst(redact_url, request) -> RedactInstance:
    service = request.param
    out_type = OutputType.overlays if service == ServiceType.extract else OutputType.images
    return RedactInstance.create(service=service, out_type=out_type, redact_url=redact_url)


@pytest.fixture
def job(any_img_redact_inst, some_image) -> RedactJob:
    return any_img_redact_inst.start_job(file=some_image)
