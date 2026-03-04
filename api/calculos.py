from django.db.models import Sum


def calcular_resumen_docente(docente, planificacion):
    """Calcula el resumen completo de carga de un docente para una planificación."""
    from .models import CargaDocente, OtraActividad

    cargas = CargaDocente.objects.filter(
        docente=docente, planificacion=planificacion
    ).select_related("modulo__asignatura")

    # Agrupar por asignatura
    por_asignatura = {}
    total_horas_directas = 0
    total_horas_indirectas = 0

    for carga in cargas:
        codigo = carga.modulo.asignatura.codigo
        if codigo not in por_asignatura:
            por_asignatura[codigo] = {
                "asignatura": carga.modulo.asignatura.nombre,
                "horas_directas": 0,
                "horas_indirectas": 0,
                "modulos": [],
            }
        por_asignatura[codigo]["horas_directas"] += carga.horas_directas
        por_asignatura[codigo]["horas_indirectas"] += carga.horas_indirectas
        por_asignatura[codigo]["modulos"].append({
            "modulo": carga.modulo.nombre,
            "cantidad": carga.cantidad,
            "unidad": carga.modulo.unidad,
            "horas_total": carga.horas_total,
            "observaciones": carga.observaciones,
        })
        total_horas_directas += carga.horas_directas
        total_horas_indirectas += carga.horas_indirectas

    total_pregrado = total_horas_directas + total_horas_indirectas

    otras = OtraActividad.objects.filter(docente=docente, planificacion=planificacion)
    total_otras = sum(o.horas for o in otras)

    total_general = total_pregrado + total_otras
    diferencia = total_general - docente.horas_contrato

    return {
        "docente": docente.get_full_name(),
        "horas_contrato": docente.horas_contrato,
        "por_asignatura": por_asignatura,
        "total_horas_directas": round(total_horas_directas, 3),
        "total_horas_indirectas": round(total_horas_indirectas, 3),
        "total_pregrado": round(total_pregrado, 3),
        "total_otras_actividades": round(total_otras, 3),
        "total_general": round(total_general, 3),
        "diferencia": round(diferencia, 3),
        "estado": calcular_estado(diferencia),
    }


def calcular_estado(diferencia):
    if diferencia > 2:
        return "exceso"
    elif diferencia < -2:
        return "deficit"
    return "equilibrio"


def calcular_resumen_planificacion(planificacion):
    """Calcula el resumen consolidado de todos los docentes."""
    from .models import Usuario

    docentes = Usuario.objects.filter(
        cargas__planificacion=planificacion
    ).distinct()

    resumen = []
    for docente in docentes:
        resumen.append(calcular_resumen_docente(docente, planificacion))

    return resumen
