from django.db import models
from users.models import User 
from datetime import timedelta

class Vaccine(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    doses_required = models.IntegerField(default=1) 
    dose_intervals = models.JSONField(default=list) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})

    def clean(self):
        """
        Ensure that dose_intervals matches doses_required - 1 (কারণ প্রথম ডোজের ব্যবধান প্রয়োজন নেই)
        """
        if len(self.dose_intervals) != self.doses_required - 1:
            raise ValueError("Dose intervals must have exactly doses_required - 1 entries.")

    def __str__(self):
        return f"{self.name} ({self.doses_required} doses, intervals {self.dose_intervals})"


class VaccinationSchedule(models.Model):
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'patient'})
    dose_dates = models.JSONField(default=list) 
    created_at = models.DateTimeField(auto_now_add=True)

    
    def save(self, *args, **kwargs):
        """
        যখন রোগী প্রথম ডোজের বুকিং করবে, তখন সকল ডোজের তারিখ গাণিতিকভাবে সেট হবে।
        """
        if not self.dose_dates:
            dose_intervals = self.vaccine.dose_intervals
            first_dose_date = kwargs.get('first_dose_date', None) or self.dose_dates[0]

            if first_dose_date:
                self.dose_dates = [first_dose_date]  # প্রথম ডোজের তারিখ
                for interval in dose_intervals:
                    self.dose_dates.append(self.dose_dates[-1] + timedelta(days=interval))  # পরবর্তী ডোজ set হচ্ছে

        super(VaccinationSchedule, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.first_name} - {self.vaccine.name} ({len(self.dose_dates)} doses)"