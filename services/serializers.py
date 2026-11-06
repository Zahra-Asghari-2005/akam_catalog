from rest_framework import serializers
from .models import ConsultationRequest
from . import models


#category
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = "__all__"


# Service Feature
class ServiceFeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ServiceFeature
        fields = ("id", "name", "description")


# Plan Feature
class PlanFeatureSerializer(serializers.ModelSerializer):

    feature = ServiceFeatureSerializer(read_only=True)

    class Meta:
        model = models.PlanFeature
        fields = ("id", "feature", "value")


# Service Plan
class ServicePlanSerializer(serializers.ModelSerializer):

    plan_features = PlanFeatureSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = models.ServicePlan
        fields = (
            "id",
            "name",
            "description",
            "badge",
            "duration",
            "is_recommended",
            "is_active",
            "plan_features",
        )


# Service Addon
class ServiceAddonSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ServiceAddon
        fields = "__all__"


# Service Option
class ServiceOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ServiceOption
        fields = "__all__"


# Service Guide
class ServiceGuideSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ServiceGuide
        fields = "__all__"


# Service Note
class ServiceNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ServiceNote
        fields = "__all__"


# Service
class ServiceSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)

    features = ServiceFeatureSerializer(
        many=True,
        read_only=True
    )

    plans = ServicePlanSerializer(
        many=True,
        read_only=True
    )

    addons = ServiceAddonSerializer(
        many=True,
        read_only=True
    )

    options = ServiceOptionSerializer(
        many=True,
        read_only=True
    )

    guides = ServiceGuideSerializer(
        many=True,
        read_only=True
    )

    notes = ServiceNoteSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = models.Service
        fields = (
            "id",
            "category",
            "title",
            "slug",
            "short_description",
            "description",
            "image_url",
            "icon",
            "is_active",
            "features",
            "plans",
            "addons",
            "options",
            "guides",
            "notes",
            "created_at",
            "updated_at",
        )

class ConsultationRequestSerializer(serializers.ModelSerializer):

    service_name = serializers.CharField(
        source="service.title",
        read_only=True
    )

    plan_name = serializers.CharField(
        source="plan.name",
        read_only=True
    )

    class Meta:
        model = ConsultationRequest

        fields = [
            "id",
            "name",
            "phone",
            "service",
            "service_name",
            "plan",
            "plan_name",
            "message",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "created_at",
            "service_name",
            "plan_name",
        ]

    def validate(self, attrs):
        service = attrs.get(
            "service",
            getattr(self.instance, "service", None)
        )

        plan = attrs.get(
            "plan",
            getattr(self.instance, "plan", None)
        )

        if plan and service and plan.service_id != service.id:
            raise serializers.ValidationError({
                "plan": "این پلن متعلق به خدمت انتخاب‌شده نیست."
            })

        if plan and not service:
            attrs["service"] = plan.service

        return attrs

class ConsultationStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsultationRequest
        fields = ["status"]

class ServiceAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Service

        fields = [
            "id",
            "category",
            "title",
            "slug",
            "short_description",
            "description",
            "image_url",
            "icon",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

class ServicePlanAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ServicePlan

        fields = [
            "id",
            "service",
            "name",
            "description",
            "badge",
            "duration",
            "is_recommended",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["id", "created_at", "updated_at"]


class PlanFeatureAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PlanFeature

        fields = [
            "id",
            "plan",
            "feature",
            "value",
        ]

        read_only_fields = ["id"]

    def validate(self, attrs):
        plan = attrs.get(
            "plan",
            getattr(self.instance, "plan", None)
        )

        feature = attrs.get(
            "feature",
            getattr(self.instance, "feature", None)
        )

        if plan and feature and plan.service_id != feature.service_id:
            raise serializers.ValidationError(
                "این ویژگی متعلق به خدمت انتخاب‌ شده برای پلن نیست."
            )

        return attrs

    def validate(self, attrs):
        plan = attrs.get("plan", getattr(self.instance, "plan", None))
        feature = attrs.get("feature", getattr(self.instance, "feature", None))

        if plan and feature and plan.service_id != feature.service_id:
            raise serializers.ValidationError(
                "این ویژگی متعلق به خدمت انتخاب‌شده برای پلن نیست."
            )

        return attrs

class ServiceFeatureAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceFeature
        fields = "__all__"


class ServiceAddonAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceAddon
        fields = "__all__"


class ServiceOptionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceOption
        fields = "__all__"


class ServiceGuideAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceGuide
        fields = "__all__"


class ServiceNoteAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceNote
        fields = "__all__"