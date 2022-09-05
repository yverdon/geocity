from .models import StepType


def step_type(request):
    return {"StepType": StepType}
