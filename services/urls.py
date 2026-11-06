
from django.urls import path

from . import views


urlpatterns = [
    path(
        "services/",
        views.ServiceListAPI.as_view(),
        name="service-list"
    ),
    path(
        "services/<slug:slug>/",
        views.ServiceDetailAPI.as_view(),
        name="service-detail"
    ),
    path(
        "categories/",
        views.CategoryListAPI.as_view(),
        name="category-list"
    ),
    path(
        "consultations/",
        views.ConsultationCreateAPI.as_view(),
        name="consultation-create"
    ),
    path(
        "admin/consultations/",
        views.ConsultationRequestListAPI.as_view(),
        name="consultation-list"
    ),
    path(
        "admin/consultations/<int:pk>/status/",
        views.ConsultationStatusUpdateAPI.as_view(),
        name="consultation-status-update"
    ),
    path(
        "admin/categories/",
        views.CategoryAdminListCreateAPI.as_view(),
        name="admin-category-list"
    ),

    path(
        "admin/categories/<int:pk>/",
        views.CategoryAdminDetailAPI.as_view(),
        name="admin-category-detail"
    ),
    path(
        "admin/services/",
        views.ServiceAdminListCreateAPI.as_view(),
        name="admin-service-list"
    ),

    path(
        "admin/services/<int:pk>/",
        views.ServiceAdminDetailAPI.as_view(),
        name="admin-service-detail"
    ),
    path(
        "admin/plans/",
        views.ServicePlanAdminListCreateAPI.as_view(),
        name="admin-plan-list"
    ),

    path(
        "admin/plans/<int:pk>/",
        views.ServicePlanAdminDetailAPI.as_view(),
        name="admin-plan-detail"
    ),

    path(
        "admin/plan-features/",
        views.PlanFeatureAdminListCreateAPI.as_view(),
        name="admin-plan-feature-list"
    ),

    path(
        "admin/plan-features/<int:pk>/",
        views.PlanFeatureAdminDetailAPI.as_view(),
        name="admin-plan-feature-detail"
    ),
  
    path(
        "admin/features/",
        views.ServiceFeatureAdminListCreateAPI.as_view()
    ),
    path(
        "admin/features/<int:pk>/",
        views.ServiceFeatureAdminDetailAPI.as_view()
    ),

   
    path(
        "admin/addons/",
        views.ServiceAddonAdminListCreateAPI.as_view()
    ),
    path(
        "admin/addons/<int:pk>/",
        views.ServiceAddonAdminDetailAPI.as_view()
    ),

  
    path(
        "admin/options/",
        views.ServiceOptionAdminListCreateAPI.as_view()
    ),
    path(
        "admin/options/<int:pk>/",
        views.ServiceOptionAdminDetailAPI.as_view()
    ),


    path(
        "admin/guides/",
        views.ServiceGuideAdminListCreateAPI.as_view()
    ),
    path(
        "admin/guides/<int:pk>/",
        views.ServiceGuideAdminDetailAPI.as_view()
    ),


    path(
        "admin/notes/",
        views.ServiceNoteAdminListCreateAPI.as_view()
    ),
    path(
        "admin/notes/<int:pk>/",
        views.ServiceNoteAdminDetailAPI.as_view()
    ),
]
