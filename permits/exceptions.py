class BadPermitRequestStatus(Exception):
    def __init__(self, permit_request):
        self.permit_request = permit_request

    def __str__(self):
        return f"<BadPermitRequestStatus: {self.permit_request}>"
