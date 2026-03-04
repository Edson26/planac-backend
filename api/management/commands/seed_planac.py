from django.core.management.base import BaseCommand
from api.models import Asignatura, ModuloAsignatura, Planificacion, Usuario, CargaDocente, OtraActividad


ASIGNATURAS = [
    {
        "codigo": "MEC-201",
        "nombre": "Enfermería en el crecimiento y desarrollo del adulto",
        "num_estudiantes": 65,
        "modulos": [
            {"nombre": "Tutoría Teoría",         "tipo": "tutoria",        "unidad": "grupos",   "factor_d": 1.0,  "factor_i": 1.0},
            {"nombre": "Clase Teoría",            "tipo": "clase",          "unidad": "periodos", "factor_d": 3.0,  "factor_i": 3.0},
            {"nombre": "Práctica Grupos",         "tipo": "grupo_practica", "unidad": "grupos",   "factor_d": 4.0,  "factor_i": 0.0},
        ]
    },
    {
        "codigo": "MEC-302",
        "nombre": "Enfermería en el adulto I",
        "num_estudiantes": 64,
        "modulos": [
            {"nombre": "Tutoría",                 "tipo": "tutoria",        "unidad": "grupos",   "factor_d": 2.5,  "factor_i": 2.5},
            {"nombre": "Clases Intensivo Teoría", "tipo": "clase",          "unidad": "periodos", "factor_d": 2.0,  "factor_i": 2.0},
            {"nombre": "Clases Práctica Clínica", "tipo": "clase",          "unidad": "periodos", "factor_d": 2.0,  "factor_i": 2.0},
            {"nombre": "SMC APS",                 "tipo": "grupo_practica", "unidad": "grupos",   "factor_d": 1.0,  "factor_i": 0.0},
            {"nombre": "Práctica APS",            "tipo": "grupo_practica", "unidad": "grupos",   "factor_d": 1.5,  "factor_i": 0.0},
            {"nombre": "SMC SM",                  "tipo": "grupo_practica", "unidad": "grupos",   "factor_d": 0.25, "factor_i": 0.0},
            {"nombre": "Práctica SM",             "tipo": "grupo_practica", "unidad": "grupos",   "factor_d": 1.25, "factor_i": 0.0},
            {"nombre": "SMC INTRA",               "tipo": "grupo_practica", "unidad": "grupos",   "factor_d": 1.5,  "factor_i": 0.0},
            {"nombre": "Práctica INTRA",          "tipo": "grupo_practica", "unidad": "grupos",   "factor_d": 5.5,  "factor_i": 0.0},
        ]
    },
    {
        "codigo": "MEC-364",
        "nombre": "Práctica Profesional Controlada",
        "num_estudiantes": 22,
        "modulos": [
            {"nombre": "PPC Intramuro (Internos)", "tipo": "grupo_practica", "unidad": "grupos", "factor_d": 2.0, "factor_i": 0.0},
        ]
    },
    {
        "codigo": "GIS-I",
        "nombre": "Gestión e Investigación en Salud I",
        "num_estudiantes": 0,
        "modulos": [
            {"nombre": "Tutoría GIS", "tipo": "tutoria", "unidad": "grupos", "factor_d": 2.5, "factor_i": 2.5},
        ]
    },
    {
        "codigo": "ENCARGATURA",
        "nombre": "Encargatura de Módulos",
        "num_estudiantes": 0,
        "modulos": [
            {"nombre": "Encargatura Teoría MEC-201",   "tipo": "encargatura", "unidad": "grupos", "factor_d": 3.0, "factor_i": 0.0},
            {"nombre": "Encargatura Práctica MEC-201", "tipo": "encargatura", "unidad": "grupos", "factor_d": 2.0, "factor_i": 0.0},
            {"nombre": "Encargatura Teoría MEC-302",   "tipo": "encargatura", "unidad": "grupos", "factor_d": 2.0, "factor_i": 0.0},
            {"nombre": "Encargatura Módulo APS",       "tipo": "encargatura", "unidad": "grupos", "factor_d": 3.0, "factor_i": 0.0},
            {"nombre": "Encargatura Módulo IH",        "tipo": "encargatura", "unidad": "grupos", "factor_d": 1.0, "factor_i": 0.0},
            {"nombre": "Encargatura Módulo SM",        "tipo": "encargatura", "unidad": "grupos", "factor_d": 1.0, "factor_i": 0.0},
            {"nombre": "Encargatura PPC Adulto",       "tipo": "encargatura", "unidad": "grupos", "factor_d": 1.0, "factor_i": 0.0},
        ]
    },
]

# Datos reales de carga extraídos del Excel
CARGAS_REALES = {
    "patricia.diaz": {
        "horas_contrato": 22,
        "cargas": [
            ("MEC-201", "Tutoría Teoría",          1),
            ("MEC-201", "Clase Teoría",             2),
            ("MEC-302", "Clases Intensivo Teoría",  8),
            ("MEC-302", "Clases Práctica Clínica",  8),
            ("MEC-364", "PPC Intramuro (Internos)", 3),
        ],
        "otras": [
            {"descripcion": "Reunión de carrera/Dpto.", "horas": 1.0},
            {"descripcion": "Atención a estudiantes", "horas": 1.0},
            {"descripcion": "Rediseño curricular", "horas": 3.0},
            {"descripcion": "Secretaría académica", "horas": 3.0},
            {"descripcion": "Diplomado", "horas": 2.0},
            {"descripcion": "Mesa Cardiovascular", "horas": 1.0},
            {"descripcion": "Proyecto investigación Fx riesgo/estilos de vida", "horas": 2.0},
        ]
    },
    "camila.alveal": {
        "horas_contrato": 33,
        "cargas": [
            ("MEC-201", "Práctica Grupos",          1),
            ("MEC-302", "Tutoría",                  1),
            ("MEC-302", "Clases Intensivo Teoría",  2),
            ("MEC-302", "Clases Práctica Clínica",  5),
            ("MEC-364", "PPC Intramuro (Internos)", 2),
            ("GIS-I",   "Tutoría GIS",              1),
        ],
        "otras": [
            {"descripcion": "Salvando vidas", "horas": 3.0},
            {"descripcion": "Atención a estudiantes", "horas": 2.0},
            {"descripcion": "Reuniones de carrera", "horas": 1.0},
            {"descripcion": "Mesa VIH", "horas": 1.0},
            {"descripcion": "Unidad infantil", "horas": 0.75},
        ]
    },
    "florencia.lastarria": {
        "horas_contrato": 22,
        "cargas": [
            ("MEC-201", "Clase Teoría",             4),
            ("MEC-302", "Clases Intensivo Teoría",  8),
        ],
        "otras": [
            {"descripcion": "Comisión de estudio", "horas": 7.0},
            {"descripcion": "Manuscritos", "horas": 3.0},
            {"descripcion": "Unidad de gestión", "horas": 10.0},
        ]
    },
    "gustavo.araneda": {
        "horas_contrato": 44,
        "cargas": [
            ("MEC-302", "Tutoría",                  1),
            ("MEC-302", "Clases Práctica Clínica",  6),
            ("MEC-364", "PPC Intramuro (Internos)", 2),
            ("GIS-I",   "Tutoría GIS",              1),
        ],
        "otras": [
            {"descripcion": "Reunión de carrera/Dpto.", "horas": 1.0},
            {"descripcion": "OFECS", "horas": 4.0},
            {"descripcion": "Comité académico de especialidad", "horas": 2.0},
            {"descripcion": "Atención a estudiantes", "horas": 2.0},
            {"descripcion": "Mesa intersectorial TBC", "horas": 1.0},
            {"descripcion": "Colaborador TD", "horas": 1.0},
            {"descripcion": "Unidad de gestión", "horas": 0.75},
            {"descripcion": "Backup Mesa VIH", "horas": 1.0},
        ]
    },
    "hernan.henriquez": {
        "horas_contrato": 11,
        "cargas": [
            ("MEC-302", "Práctica SM",              6),
            ("MEC-302", "SMC SM",                   6),
            ("MEC-364", "PPC Intramuro (Internos)", 1),
        ],
        "otras": [
            {"descripcion": "Otras actividades", "horas": 1.0},
        ]
    },
    "laura.carvallo": {
        "horas_contrato": 44,
        "cargas": [
            ("MEC-302", "Tutoría",                  1),
            ("MEC-364", "PPC Intramuro (Internos)", 4),
            ("GIS-I",   "Tutoría GIS",              1),
        ],
        "otras": [
            {"descripcion": "Otras actividades (detalle pendiente)", "horas": 23.0},
        ]
    },
    "lucciana.leonelli": {
        "horas_contrato": 33,
        "cargas": [
            ("MEC-201", "Práctica Grupos",          1),
            ("MEC-302", "Tutoría",                  1),
            ("MEC-302", "Clases Intensivo Teoría",  4),
            ("MEC-302", "Clases Práctica Clínica",  8),
            ("MEC-302", "SMC INTRA",                3),
            ("MEC-302", "Práctica INTRA",           1),
            ("MEC-364", "PPC Intramuro (Internos)", 2),
            ("ENCARGATURA", "Encargatura Práctica MEC-201", 1),
        ],
        "otras": [
            {"descripcion": "Atención a estudiantes", "horas": 2.0},
            {"descripcion": "Reunión de carrera y departamento", "horas": 1.0},
            {"descripcion": "Master", "horas": 3.0},
            {"descripcion": "Salvando vidas", "horas": 2.0},
            {"descripcion": "Colaborador TD", "horas": 1.0},
        ]
    },
    "david.ugarte": {
        "horas_contrato": 33,
        "cargas": [
            ("MEC-201", "Tutoría Teoría",           1),
            ("MEC-201", "Clase Teoría",             14),
            ("MEC-201", "Práctica Grupos",          2),
            ("MEC-302", "Clases Intensivo Teoría",  4),
            ("MEC-302", "Clases Práctica Clínica",  4),
            ("MEC-302", "Práctica SM",              10),
            ("MEC-302", "SMC SM",                   10),
            ("MEC-364", "PPC Intramuro (Internos)", 2),
            ("ENCARGATURA", "Encargatura Módulo SM", 1),
        ],
        "otras": [
            {"descripcion": "Proyecto PAC Psiquiatría (RI 056)", "horas": 1.0},
            {"descripcion": "Proyecto Aprendizaje+Servicio+Counselling", "horas": 1.0},
            {"descripcion": "Atención a estudiantes", "horas": 2.0},
            {"descripcion": "Reunión Dpto. y carrera", "horas": 1.0},
            {"descripcion": "Mesa intercultural", "horas": 1.0},
            {"descripcion": "Mesa prevención del suicidio", "horas": 1.0},
            {"descripcion": "Encargatura de práctica + módulo", "horas": 3.0},
        ]
    },
    "maria.romo": {
        "horas_contrato": 44,
        "cargas": [
            ("MEC-201", "Tutoría Teoría",           1),
            ("MEC-201", "Clase Teoría",             2),
            ("MEC-201", "Práctica Grupos",          2),
            ("MEC-364", "PPC Intramuro (Internos)", 1),
            ("GIS-I",   "Tutoría GIS",              1),
        ],
        "otras": [
            {"descripcion": "OFECS", "horas": 4.0},
            {"descripcion": "Encargatura GIS I", "horas": 3.0},
            {"descripcion": "Atención de estudiantes", "horas": 2.0},
            {"descripcion": "Reunión de carrera", "horas": 1.0},
            {"descripcion": "Comité académico de especialidad", "horas": 2.0},
            {"descripcion": "Mesa intersectorial del Cáncer", "horas": 1.0},
            {"descripcion": "DIUFRO", "horas": 4.0},
            {"descripcion": "Unidad de gestión", "horas": 8.75},
        ]
    },
    "marcelo.aedo": {
        "horas_contrato": 44,
        "cargas": [
            ("MEC-302", "Tutoría",                  1),
            ("MEC-302", "Clases Intensivo Teoría",  11),
            ("MEC-302", "Clases Práctica Clínica",  8),
            ("MEC-302", "SMC INTRA",                3),
            ("MEC-302", "Práctica INTRA",           1),
            ("MEC-364", "PPC Intramuro (Internos)", 2),
        ],
        "otras": [
            {"descripcion": "Reunión de carrera/Dpto.", "horas": 1.0},
            {"descripcion": "Encargatura GES", "horas": 2.0},
            {"descripcion": "Atención de estudiantes", "horas": 2.0},
            {"descripcion": "Presidente Comité Paritario", "horas": 3.0},
            {"descripcion": "Fortalece academia: Centilena Oncológico", "horas": 3.0},
            {"descripcion": "Tu puedes salvar vidas", "horas": 2.0},
            {"descripcion": "Back-Up Mesa regional del cáncer", "horas": 1.0},
            {"descripcion": "Aplicación CEAL", "horas": 2.0},
            {"descripcion": "Transformación digital enfermería adulto", "horas": 2.0},
            {"descripcion": "Encargado área VcM", "horas": 3.0},
        ]
    },
    "rocio.ferrada": {
        "horas_contrato": 44,
        "cargas": [
            ("MEC-201", "Tutoría Teoría",           1),
            ("MEC-201", "Clase Teoría",             13),
            ("MEC-302", "SMC APS",                  8),
            ("ENCARGATURA", "Encargatura Módulo APS", 1),
        ],
        "otras": [
            {"descripcion": "Unidad de gestión", "horas": 11.14},
            {"descripcion": "Reunión Dpto./carrera", "horas": 1.0},
            {"descripcion": "Atención de estudiantes", "horas": 2.0},
            {"descripcion": "Comité curricular", "horas": 2.0},
            {"descripcion": "Rediseño curricular", "horas": 2.0},
            {"descripcion": "Comité académico especialidades", "horas": 2.0},
            {"descripcion": "Mesa persona mayor", "horas": 1.0},
            {"descripcion": "Mesa interculturalidad", "horas": 1.0},
            {"descripcion": "DIUFRO PEG 250016", "horas": 4.0},
            {"descripcion": "Encargada de unidad y PPC Extra", "horas": 1.0},
        ]
    },
    "rigo.torres": {
        "horas_contrato": 44,
        "cargas": [
            ("MEC-201", "Tutoría Teoría",           1),
            ("MEC-201", "Clase Teoría",             17),
            ("MEC-201", "Práctica Grupos",          1),
            ("ENCARGATURA", "Encargatura Teoría MEC-201", 1),
        ],
        "otras": [
            {"descripcion": "VCM", "horas": 22.0},
            {"descripcion": "Rediseño curricular", "horas": 2.0},
            {"descripcion": "Comité curricular", "horas": 2.0},
            {"descripcion": "Atención a estudiantes", "horas": 1.0},
            {"descripcion": "Reunión de carrera", "horas": 1.0},
            {"descripcion": "Proyecto inv. APS Pitrufquén Ultraestación", "horas": 2.0},
            {"descripcion": "SMC del Adulto + Encargatura", "horas": 5.0},
            {"descripcion": "Encargatura de teoría", "horas": 2.0},
            {"descripcion": "Encargatura de unidad", "horas": 3.0},
        ]
    },
    "claudio.carcamo": {
        "horas_contrato": 22,
        "cargas": [
            ("MEC-302", "Tutoría",                  1),
            ("MEC-302", "Clases Intensivo Teoría",  6),
            ("MEC-302", "Clases Práctica Clínica",  4),
            ("MEC-364", "PPC Intramuro (Internos)", 2),
            ("ENCARGATURA", "Encargatura PPC Adulto", 1),
        ],
        "otras": [
            {"descripcion": "Reuniones de carrera/Dpto.", "horas": 1.0},
            {"descripcion": "Encargatura", "horas": 3.0},
            {"descripcion": "Atención a estudiantes", "horas": 1.0},
            {"descripcion": "Comité académico de especialidades", "horas": 2.0},
            {"descripcion": "Proyecto de sustentabilidad", "horas": 2.0},
        ]
    },
}


class Command(BaseCommand):
    help = "Carga todos los datos reales del PLANAC 2026 - 1er Semestre"

    def handle(self, *args, **kwargs):
        # 1. Crear planificación
        plan, _ = Planificacion.objects.get_or_create(
            anio=2026, semestre=1, defaults={"activo": True}
        )
        self.stdout.write(self.style.SUCCESS(f"✓ Planificación: {plan}"))

        # 2. Crear asignaturas y módulos
        modulo_map = {}  # (codigo_asig, nombre_modulo) -> ModuloAsignatura
        for asig_data in ASIGNATURAS:
            asig, _ = Asignatura.objects.get_or_create(
                codigo=asig_data["codigo"],
                defaults={
                    "nombre": asig_data["nombre"],
                    "num_estudiantes": asig_data["num_estudiantes"],
                }
            )
            for mod_data in asig_data["modulos"]:
                mod, _ = ModuloAsignatura.objects.get_or_create(
                    asignatura=asig,
                    nombre=mod_data["nombre"],
                    defaults={
                        "tipo": mod_data["tipo"],
                        "unidad": mod_data["unidad"],
                        "factor_d": mod_data["factor_d"],
                        "factor_i": mod_data["factor_i"],
                    }
                )
                modulo_map[(asig_data["codigo"], mod_data["nombre"])] = mod
            self.stdout.write(f"  ✓ {asig_data['codigo']}: {len(asig_data['modulos'])} módulos")

        # 3. Cargar datos reales por docente
        for username, data in CARGAS_REALES.items():
            try:
                docente = Usuario.objects.get(username=username)
                # Actualizar horas de contrato
                docente.horas_contrato = data["horas_contrato"]
                docente.save()

                # Cargar cargas
                for codigo_asig, nombre_mod, cantidad in data["cargas"]:
                    modulo = modulo_map.get((codigo_asig, nombre_mod))
                    if modulo:
                        CargaDocente.objects.update_or_create(
                            planificacion=plan, docente=docente, modulo=modulo,
                            defaults={"cantidad": cantidad}
                        )

                # Cargar otras actividades
                OtraActividad.objects.filter(planificacion=plan, docente=docente).delete()
                for act in data["otras"]:
                    OtraActividad.objects.create(
                        planificacion=plan,
                        docente=docente,
                        descripcion=act["descripcion"],
                        horas=act["horas"],
                    )
                self.stdout.write(self.style.SUCCESS(f"  ✓ {username}"))
            except Usuario.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"  ⚠ Usuario no encontrado: {username} (ejecuta primero cargar_docentes)"))

        self.stdout.write(self.style.SUCCESS("\n✓ Seed completado. PLANAC 2026-1 cargado en la base de datos."))
