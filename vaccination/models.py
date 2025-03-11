from django.db import models
from users.models import User 

class Vaccine(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})

    def __str__(self):
        return self.name

class VaccinationSchedule(models.Model):
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'patient'})
    date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedule_creator")

    def __str__(self):
        return f"{self.vaccine.name} for {self.patient.phone_number} on {self.date}"
