import time
import logging

from fastapi import Request


logger = logging.getLogger(__name__)


async def log_request(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        "%s %s - %.4fs",
        request.method,
        request.url.path,
        process_time
    )

    return response