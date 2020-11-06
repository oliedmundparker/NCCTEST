from django.db import models


class User(models.Model):
    """
    User model to describe details about a user.
    """
    username = models.CharField(max_length=30)
    email = models.EmailField()
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Scanner(models.Model):
    """
    Scanner model to have a table of valid scanners that can be run.
    """
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Assets(models.Model):
    """
    Asset model to describe details about an asset a scan can be run on.
    """
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    created = models.DateTimeField()

    def __str__(self):
        return self.name

# Some status options for choices in the Scan class. Note that this is more foresight than a requirement.
StatusChoices = (
    ("COMPLETE", "complete"),
    ("failed", "FAILED"),
    ("STARTED", "started"),
    ("NOTSTARTED", "not started")
)


# Create a tuple of user information for validation against the requested_by field in the Scan model.
UserChoices = [(user.id, user.pk) for user in User.objects.all()]


class Scan(models.Model):
    """
    Scan model to describe details about a Scan that has been performed.
    """
    requested_by = models.ForeignKey(User, choices=UserChoices, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=StatusChoices)
    scanners = models.ManyToManyField(Scanner)
    assets_scanned = models.ManyToManyField(Assets)

    def __str__(self):
        return "{} requested by {} at {}".format(self.name, self.requested_by, self.started_at)


class SeverityCounts(models.Model):
    """
    SevrityCounts model to describe the types of errors that occurred during a scan. Has a 1-1 relationship with a Scan
    object.
    """
    critical = models.IntegerField()
    high = models.IntegerField()
    medium = models.IntegerField()
    low = models.IntegerField()
    information = models.IntegerField()
    scan = models.OneToOneField(Scan, on_delete=models.CASCADE, primary_key=True, related_name='severity_counts')


# Types of errors we have.
SeverityChoices = (
    ("CRITICAL", "critical"),
    ("HIGH", "high"),
    ("MEDIUM", "medium"),
    ("LOW", "low"),
    ("INFORMATION", "information"),
)


class Vulnerability(models.Model):
    """
    Vulnerability object to describe a particular vulnerability found during a scan.
    """
    from_scan = models.ForeignKey(Scan, on_delete=models.CASCADE)
    severity_score = models.CharField(max_length=11, choices=SeverityChoices)
    name = models.CharField(max_length=20)
    description = models.TextField()
    solution = models.TextField(blank=True)
    references = models.URLField(blank=True)
    cvss_base_score = models.FloatField()
    affected_assets = models.ManyToManyField(Assets)

    def __str__(self):
        return self.name