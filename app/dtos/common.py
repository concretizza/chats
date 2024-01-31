from http import HTTPStatus

NotFoundResponse = {
    HTTPStatus.NOT_FOUND.value: {"description": HTTPStatus.NOT_FOUND.phrase},
}
