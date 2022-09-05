class BadPermitRequestStatus(Exception):
    def __init__(self, permit_request, expected_status):
        self.permit_request = permit_request
        self.expected_status = expected_status

    def __str__(self):
        return "Bad permit request status {}, expected one of {}".format(
            self.permit_request.status, self.expected_status
        )


class NonProlongablePermitRequest(Exception):
    def __str__(self):
        return "The permit cannot be prolonged"
