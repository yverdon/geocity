class BadSubmissionStatus(Exception):
    def __init__(self, submission, expected_status):
        self.submission = submission
        self.expected_status = expected_status

    def __str__(self):
        return "Bad submission status {}, expected one of {}".format(
            self.submission.status, self.expected_status
        )


class NonProlongableSubmission(Exception):
    def __str__(self):
        return "The permit cannot be prolonged"
