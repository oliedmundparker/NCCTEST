from .models import User, Scan, Vulnerability, Assets, SeverityCounts
from rest_framework import serializers


class SeverityCountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeverityCounts
        fields = ['critical', 'high', 'medium', 'low', 'information']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = ['id', 'requested_by', 'started_at', 'finished_at', 'name', 'status', 'scanners', 'severity_counts',
                  'assets_scanned']

    severity_counts = SeverityCountsSerializer()

    def create(self, validated_data):
        scan = Scan(
            requested_by=validated_data['requested_by'],
            started_at=validated_data['started_at'],
            finished_at=validated_data['finished_at'],
            name=validated_data['name'],
            status=validated_data['status']
        )
        scan.save()
        scan.scanners.set(validated_data['scanners'])
        scan.assets_scanned.set(validated_data['assets_scanned'])
        scan.save()

        severity_counts_data = validated_data['severity_counts']
        severity_counts = SeverityCounts(
            critical=severity_counts_data['critical'],
            high=severity_counts_data['high'],
            medium=severity_counts_data['medium'],
            low=severity_counts_data['low'],
            information=severity_counts_data['information'],
            scan=scan
        )
        severity_counts.save()

        return scan

    def update(self, instance, validated_data):
        instance.requested_by = validated_data['requested_by']
        instance.started_at = validated_data['started_at']
        instance.finished_at = validated_data['finished_at']
        instance.name = validated_data['name']
        instance.status = validated_data['status']

        instance.scanners.set(validated_data['scanners'])
        instance.assets_scanned.set(validated_data['assets_scanned'])

        severity_counts_instance = instance.severity_counts
        severity_counts_data = validated_data['severity_counts']
        severity_counts_instance.critical = severity_counts_data['critical']
        severity_counts_instance.high = severity_counts_data['high']
        severity_counts_instance.medium = severity_counts_data['medium']
        severity_counts_instance.low = severity_counts_data['low']
        severity_counts_instance.information = severity_counts_data['information']
        severity_counts_instance.scan = instance

        return instance


class AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assets
        fields = ['id', 'name', 'description', 'created']


class VulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = ['id', 'from_scan', 'severity_score', 'name', 'description', 'solution', 'references', 'cvss_base_score',
                  "affected_assets"]

    def create(self, validated_data):
        vulnerability = Vulnerability(
            from_scan=validated_data['from_scan'],
            severity_score=validated_data['severity_score'],
            name=validated_data['name'],
            description=validated_data['description'],
            solution=validated_data['solution'],
            references=validated_data['references'],
            cvss_base_score=validated_data['cvss_base_score']
        )
        vulnerability.save()
        vulnerability.affected_assets.set(validated_data['affected_assets'])

        return vulnerability

    def update(self, instance, validated_data):
        instance.from_scan = validated_data['from_scan']
        instance.severity_score = validated_data['severity_score']
        instance.name = validated_data['name']
        instance.description = validated_data['description']
        instance.solution = validated_data['solution']
        instance.references = validated_data['references']
        instance.cvss_base_score = validated_data['cvss_base_score']
        instance.affected_assets.set(validated_data['affected_assets'])

        return instance
