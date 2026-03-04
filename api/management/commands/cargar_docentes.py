from django.core.management.base import BaseCommand
from api.models import Usuario

DOCENTES = [
    {"username": "patricia.diaz",      "first_name": "Ma. Patricia", "last_name": "Díaz",      "horas_contrato": 44, "rol": "docente"},
    {"username": "camila.alveal",       "first_name": "Camila",       "last_name": "Alveal",     "horas_contrato": 44, "rol": "docente"},
    {"username": "gustavo.araneda",     "first_name": "Gustavo",      "last_name": "Araneda",    "horas_contrato": 44, "rol": "docente"},
    {"username": "lucciana.leonelli",   "first_name": "Lucciana",     "last_name": "Leonelli",   "horas_contrato": 44, "rol": "coordinador"},
    {"username": "rigo.torres",         "first_name": "Rigo",         "last_name": "Torres",     "horas_contrato": 44, "rol": "coordinador"},
    {"username": "david.ugarte",        "first_name": "David",        "last_name": "Ugarte",     "horas_contrato": 44, "rol": "docente"},
    {"username": "rocio.ferrada",       "first_name": "Rocío",        "last_name": "Ferrada",    "horas_contrato": 44, "rol": "docente"},
    {"username": "marcelo.aedo",        "first_name": "Marcelo",      "last_name": "Aedo",       "horas_contrato": 44, "rol": "docente"},
    {"username": "claudio.carcamo",     "first_name": "Claudio",      "last_name": "Cárcamo",    "horas_contrato": 22, "rol": "docente"},
    {"username": "hernan.henriquez",    "first_name": "Hernán",       "last_name": "Henríquez",  "horas_contrato": 22, "rol": "docente"},
    {"username": "laura.carvallo",      "first_name": "Laura",        "last_name": "Carvallo",   "horas_contrato": 44, "rol": "docente"},
    {"username": "maria.romo",          "first_name": "María Teresa", "last_name": "Romo",       "horas_contrato": 44, "rol": "docente"},
    {"username": "florencia.lastarria", "first_name": "Florencia",    "last_name": "Lastarria",  "horas_contrato": 22, "rol": "docente"},
]

class Command(BaseCommand):
    help = "Carga los docentes del PLANAC 2026"

    def handle(self, *args, **kwargs):
        for d in DOCENTES:
            user, created = Usuario.objects.get_or_create(
                username=d["username"],
                defaults={
                    "first_name": d["first_name"],
                    "last_name": d["last_name"],
                    "horas_contrato": d["horas_contrato"],
                    "rol": d["rol"],
                }
            )
            if created:
                user.set_password("Planac2026!")  # contraseña temporal
                user.save()
                self.stdout.write(self.style.SUCCESS(f"✓ Creado: {d['username']}"))
            else:
                self.stdout.write(f"  Ya existe: {d['username']}")
