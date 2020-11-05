from enum import Enum

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    first_name = models.CharField(max_length=12)
    last_name = models.CharField(max_length=12)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Scanner(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Assets(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    created = models.DateTimeField()

    def __str__(self):
        return self.name

StatusOptions = (
    ("COMPLETE", "complete"),
    ("STARTED", "started"),
    ("NOTSTARTED", "not started")
)


class Scan(models.Model):
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at = models.DateTimeField()
    finished_At = models.DateTimeField()
    status = models.CharField(max_length=20, choices=StatusOptions)
    scanners = models.ManyToManyField(Scanner)
    assets_scanned = models.ManyToManyField(Assets)

    def __str__(self):
        return "Scan requested by {} at {}".format(self.requested_by, self.started_at)


class SeverityCounts(models.Model):
    critical = models.IntegerField()
    high = models.IntegerField()
    medium = models.IntegerField()
    low = models.IntegerField()
    information = models.IntegerField()
    scan = models.OneToOneField(Scan, on_delete=models.CASCADE)


SeverityChoices = (
    ("CRITICAL", "critical"),
    ("HIGH", "high"),
    ("MEDIUM", "medium"),
    ("LOW", "low"),
    ("INFORMATION", "information"),
)


class Vulnerability(models.Model):
    from_scan = models.ForeignKey(Scan, on_delete=models.CASCADE)
    severity_score = models.CharField(max_length=11, choices=SeverityChoices)
    name = models.CharField(max_length=20)
    description = models.TextField()
    solution = models.TextField(blank=True)
    references = models.URLField(blank=True)
    cvss_base_scare = models.FloatField()
    affected_assets = models.ManyToManyField(Assets)

    def __str__(self):
        return self.name