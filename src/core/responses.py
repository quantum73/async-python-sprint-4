from fastapi import status
from fastapi.responses import Response

GoneResponse = Response(status_code=status.HTTP_410_GONE)
MaxBatchSizeResponse = Response(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
