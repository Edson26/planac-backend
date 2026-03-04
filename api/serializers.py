from rest_framework import serializers
from .models import Usuario, Planificacion, Asignatura, ModuloAsignatura, CargaDocente, OtraActividad
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "username", "first_name", "last_name", "email", "rol", "horas_contrato"]
        read_only_fields = ["username"]


class AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignatura
        fields = "__all__"


class ModuloAsignaturaSerializer(serializers.ModelSerializer):
    asignatura_nombre = serializers.CharField(source="asignatura.nombre", read_only=True)
    asignatura_codigo = serializers.CharField(source="asignatura.codigo", read_only=True)

    class Meta:
        model = ModuloAsignatura
        fields = "__all__"


class CargaDocenteSerializer(serializers.ModelSerializer):
    modulo_nombre = serializers.CharField(source="modulo.nombre", read_only=True)
    asignatura_codigo = serializers.CharField(source="modulo.asignatura.codigo", read_only=True)
    asignatura_nombre = serializers.CharField(source="modulo.asignatura.nombre", read_only=True)
    horas_directas = serializers.FloatField(read_only=True)
    horas_indirectas = serializers.FloatField(read_only=True)
    horas_total = serializers.FloatField(read_only=True)
    unidad = serializers.CharField(source="modulo.unidad", read_only=True)

    class Meta:
        model = CargaDocente
        fields = "__all__"


class OtraActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtraActividad
        fields = "__all__"


class PlanificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planificacion
        fields = "__all__"

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Incluir datos del usuario directamente en el token
        token["user"] = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "rol": user.rol,
            "horas_contrato": user.horas_contrato,
        }
        return token
