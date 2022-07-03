from domain.primaryports import GenerateMosaicCommand
from domain.representations import SuccessResponse, BadRequestResponse, ErrorResponse
from mediatr import Mediator
from typing import Union


@Mediator.handler
class GenerateMosaicCommandHandler:
    async def handle(self, request: GenerateMosaicCommand) -> Union[SuccessResponse, BadRequestResponse, ErrorResponse]:
        return SuccessResponse()
