
from django.contrib import admin

from . import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")


# -------------------------
# Service Inlines
# -------------------------

class ServiceFeatureInline(admin.TabularInline):
    model = models.ServiceFeature
    extra = 0


class ServicePlanInline(admin.TabularInline):
    model = models.ServicePlan
    extra = 0
    show_change_link = True


class ServiceAddonInline(admin.TabularInline):
    model = models.ServiceAddon
    extra = 0


class ServiceOptionInline(admin.TabularInline):
    model = models.ServiceOption
    extra = 0


class ServiceGuideInline(admin.TabularInline):
    model = models.ServiceGuide
    extra = 0


class ServiceNoteInline(admin.TabularInline):
    model = models.ServiceNote
    extra = 0


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "is_active",
        "created_at",
    )

    list_filter = ("category", "is_active")
    search_fields = ("title", "description", "short_description")
    prepopulated_fields = {"slug": ("title",)}

    readonly_fields = ("created_at", "updated_at")

    inlines = [
        ServiceFeatureInline,
        ServicePlanInline,
        ServiceAddonInline,
        ServiceOptionInline,
        ServiceGuideInline,
        ServiceNoteInline,
    ]


class PlanFeatureInline(admin.TabularInline):
    model = models.PlanFeature
    extra = 0


@admin.register(models.ServicePlan)
class ServicePlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "service",
        "is_recommended",
        "is_active",
    )

    list_filter = ("service", "is_recommended", "is_active")
    search_fields = ("name", "service__title")

    inlines = [PlanFeatureInline]


@admin.register(models.PlanFeature)
class PlanFeatureAdmin(admin.ModelAdmin):
    list_display = ("plan", "feature", "value")
    list_filter = ("plan__service",)
    search_fields = (
        "plan__name",
        "feature__name",
    )


@admin.register(models.ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "service",
        "plan",
        "status",
        "created_at",
    )

    list_filter = ("status", "created_at")
    search_fields = ("name", "phone", "message")

    readonly_fields = ("created_at",)

    list_editable = ("status",)

    date_hierarchy = "created_at"



@admin.register(models.ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ("name", "service")
    list_filter = ("service",)
    search_fields = ("name", "description", "service__title")