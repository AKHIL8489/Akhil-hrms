import random
from .models import *

def generate_employee_code():
    latest_user = User.objects.order_by('-id').first()
    latestAddedEmployee = latest_user.emplyeeIdentficationCode
    numeric_part = int(latestAddedEmployee.split('-')[1])
    new_numeric_part = numeric_part + 1
    newEmployeeCode = f"MT-{new_numeric_part:05d}"
    return newEmployeeCode