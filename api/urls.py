from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet, PlanificacionViewSet, AsignaturaViewSet,
    ModuloAsignaturaViewSet, CargaDocenteViewSet, OtraActividadViewSet
)

router = DefaultRouter()
router.register("usuarios", UsuarioViewSet)
router.register("planificaciones", PlanificacionViewSet)
router.register("asignaturas", AsignaturaViewSet)
router.register("modulos", ModuloAsignaturaViewSet)
router.register("cargas", CargaDocenteViewSet)
router.register("otras-actividades", OtraActividadViewSet)

urlpatterns = [path("", include(router.urls))]
