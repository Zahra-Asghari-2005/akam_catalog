from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from django.db.models.deletion import ProtectedError

from . import models
from . import serializers


class ServiceListAPI(GenericAPIView):

    serializer_class = serializers.ServiceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            models.Service.objects
            .filter(is_active=True)
            .select_related("category")
            .prefetch_related(
                "features",
                "plans",
                "plans__plan_features__feature",
                "addons",
                "options",
                "guides",
                "notes",
            )
        )

    def get(self, request, *args, **kwargs):

        services = self.get_queryset()

        serializer = self.get_serializer(
            services,
            many=True
        )

        return Response(serializer.data)

class ServiceDetailAPI(ServiceListAPI):
    lookup_field = "slug"

    def get(self, request, slug):
        service = self.get_object()

        serializer = self.get_serializer(service)

        return Response(serializer.data)

class CategoryListAPI(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        return models.Category.objects.all()

    def get(self, request):
        categories = self.get_queryset()

        serializer = self.get_serializer(
            categories,
            many=True
        )

        return Response(serializer.data) 

class ConsultationCreateAPI(GenericAPIView):
    queryset = models.ConsultationRequest.objects.all()
    serializer_class = serializers.ConsultationRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class ConsultationRequestListAPI(GenericAPIView):
    queryset = models.ConsultationRequest.objects.all()
    serializer_class = serializers.ConsultationRequestSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return models.ConsultationRequest.objects.all().order_by("-created_at")

    def get(self, request):
        requests = self.get_queryset()

        serializer = self.get_serializer(
            requests,
            many=True
        )

        return Response(serializer.data)

class ConsultationStatusUpdateAPI(GenericAPIView):
    queryset = models.ConsultationRequest.objects.all()
    serializer_class = serializers.ConsultationStatusSerializer
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        consultation = self.get_object()

        serializer = self.get_serializer(
            consultation,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryAdminListCreateAPI(GenericAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return models.Category.objects.all().order_by("id")

    def get(self, request):
        categories = self.get_queryset()

        serializer = self.get_serializer(
            categories,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class CategoryAdminDetailAPI(GenericAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        category = self.get_object()

        serializer = self.get_serializer(category)

        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object()

        serializer = self.get_serializer(
            category,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def patch(self, request, pk):
        category = self.get_object()

        serializer = self.get_serializer(
            category,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        category = self.get_object()

        try:
            category.delete()

        except ProtectedError:
            return Response(
                {
                    "detail": "این دسته‌بندی دارای خدمات مرتبط است و قابل حذف نیست."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

class ServiceAdminListCreateAPI(GenericAPIView):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceAdminSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return models.Service.objects.select_related("category").order_by("-created_at")

    def get(self, request):
        services = self.get_queryset()

        serializer = self.get_serializer(
            services,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class ServiceAdminDetailAPI(GenericAPIView):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceAdminSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return models.Service.objects.select_related("category")

    def get(self, request, pk):
        service = self.get_object()

        serializer = self.get_serializer(service)

        return Response(serializer.data)

    def put(self, request, pk):
        service = self.get_object()

        serializer = self.get_serializer(
            service,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def patch(self, request, pk):
        service = self.get_object()

        serializer = self.get_serializer(
            service,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        service = self.get_object()
        service.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ServicePlanAdminListCreateAPI(GenericAPIView):
    queryset = serializers.ServicePlan.objects.all()
    serializer_class = serializers.ServicePlanAdminSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = serializers.ServicePlan.objects.select_related("service")

        service_id = self.request.query_params.get("service")

        if service_id:
            queryset = queryset.filter(service_id=service_id)

        return queryset.order_by("id")

    def get(self, request):
        serializer = self.get_serializer(
            self.get_queryset(),
            many=True
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class ServicePlanAdminDetailAPI(GenericAPIView):
    queryset = serializers.ServicePlan.objects.all()
    serializer_class = serializers.ServicePlanAdminSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        plan = self.get_object()
        return Response(self.get_serializer(plan).data)

    def put(self, request, pk):
        plan = self.get_object()
        serializer = self.get_serializer(plan, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        plan = self.get_object()
        serializer = self.get_serializer(
            plan,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        plan = self.get_object()
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlanFeatureAdminListCreateAPI(GenericAPIView):
    queryset = models.PlanFeature.objects.all()
    serializer_class = serializers.PlanFeatureAdminSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = models.PlanFeature.objects.select_related(
            "plan", "feature"
        )

        plan_id = self.request.query_params.get("plan")

        if plan_id:
            queryset = queryset.filter(plan_id=plan_id)

        return queryset

    def get(self, request):
        serializer = self.get_serializer(
            self.get_queryset(),
            many=True
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class PlanFeatureAdminDetailAPI(GenericAPIView):
    queryset = models.PlanFeature.objects.all()
    serializer_class = serializers.PlanFeatureAdminSerializer
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        plan_feature = self.get_object()

        serializer = self.get_serializer(
            plan_feature,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        plan_feature = self.get_object()
        plan_feature.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class AdminListCreateAPI(GenericAPIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()

        service_id = self.request.query_params.get("service")

        if service_id and hasattr(queryset.model, "service_id"):
            queryset = queryset.filter(service_id=service_id)

        return queryset

    def get(self, request):
        serializer = self.get_serializer(
            self.get_queryset(),
            many=True
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class AdminDetailAPI(GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        obj = self.get_object()
        return Response(self.get_serializer(obj).data)

    def put(self, request, pk):
        obj = self.get_object()

        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def patch(self, request, pk):
        obj = self.get_object()

        serializer = self.get_serializer(
            obj,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        obj = self.get_object()
        obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ServiceFeatureAdminListCreateAPI(AdminListCreateAPI):
    queryset = models.ServiceFeature.objects.all()
    serializer_class = serializers.ServiceFeatureAdminSerializer


class ServiceFeatureAdminDetailAPI(AdminDetailAPI):
    queryset = models.ServiceFeature.objects.all()
    serializer_class = serializers.ServiceFeatureAdminSerializer


class ServiceAddonAdminListCreateAPI(AdminListCreateAPI):
    queryset = models.ServiceAddon.objects.all()
    serializer_class = serializers.ServiceAddonAdminSerializer


class ServiceAddonAdminDetailAPI(AdminDetailAPI):
    queryset = models.ServiceAddon.objects.all()
    serializer_class = serializers.ServiceAddonAdminSerializer


class ServiceOptionAdminListCreateAPI(AdminListCreateAPI):
    queryset = models.ServiceOption.objects.all()
    serializer_class = serializers.ServiceOptionAdminSerializer


class ServiceOptionAdminDetailAPI(AdminDetailAPI):
    queryset = models.ServiceOption.objects.all()
    serializer_class = serializers.ServiceOptionAdminSerializer


class ServiceGuideAdminListCreateAPI(AdminListCreateAPI):
    queryset = models.ServiceGuide.objects.all()
    serializer_class = serializers.ServiceGuideAdminSerializer


class ServiceGuideAdminDetailAPI(AdminDetailAPI):
    queryset = models.ServiceGuide.objects.all()
    serializer_class = serializers.ServiceGuideAdminSerializer


class ServiceNoteAdminListCreateAPI(AdminListCreateAPI):
    queryset = models.ServiceNote.objects.all()
    serializer_class = serializers.ServiceNoteAdminSerializer


class ServiceNoteAdminDetailAPI(AdminDetailAPI):
    queryset = models.ServiceNote.objects.all()
    serializer_class = serializers.ServiceNoteAdminSerializer