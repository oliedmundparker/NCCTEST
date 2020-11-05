from django.contrib import admin
from .models import User, Scan, Scanner, SeverityCounts, Assets, Vulnerability

# Register your models here.

class ScanInline(admin.StackedInline):
    model = SeverityCounts


class ScanAdmin(admin.ModelAdmin):
    inlines = [ScanInline]


admin.site.register(User)
admin.site.register(Scanner)
admin.site.register(Assets)
admin.site.register(Scan, ScanAdmin)
admin.site.register(Vulnerability)
