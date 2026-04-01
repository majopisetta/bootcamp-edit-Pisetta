#!/usr/bin/env python
"""
django-demo.py — Demo minimalista de Django sin base de datos.
Las tareas se guardan en memoria (se borran al reiniciar el servidor).

Uso:
    python django-demo.py runserver
"""
import os
import sys
from django.conf import settings
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context

# ─── Configuración mínima ────────────────────────────────────────────────────

settings.configure(
    DEBUG=True,
    SECRET_KEY="clave-secreta-solo-para-demo",
    ALLOWED_HOSTS=["*"],
    ROOT_URLCONF=__name__,
    TEMPLATES=[{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": False,
        "OPTIONS": {"context_processors": []},
    }],
    MIDDLEWARE=[
        "django.middleware.common.CommonMiddleware",
    ],
)

# ─── "Base de datos" en memoria ──────────────────────────────────────────────

tareas = []
contador = 0  # ID autoincremental


# ─── Template HTML ───────────────────────────────────────────────────────────

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Django Demo</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 600px; margin: 40px auto; padding: 0 1rem; background: #f5f5f0; color: #1a1a18; }
    h1   { font-size: 1.5rem; margin-bottom: 1.5rem; }
    form { display: flex; gap: 0.5rem; margin-bottom: 2rem; }
    input[type=text] { flex: 1; padding: 0.5rem 0.75rem; border: 1px solid #ccc; border-radius: 8px; font-size: 0.95rem; }
    button { padding: 0.5rem 1rem; border: none; border-radius: 8px; cursor: pointer; font-size: 0.9rem; }
    .btn-add  { background: #1a1a18; color: white; }
    .btn-done { background: #2d7a4f; color: white; font-size: 0.8rem; padding: 0.3rem 0.6rem; }
    .btn-del  { background: #c0392b; color: white; font-size: 0.8rem; padding: 0.3rem 0.6rem; }
    ul   { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 0.5rem; }
    li   { background: white; border: 1px solid #e0ddd6; border-radius: 10px; padding: 0.75rem 1rem; display: flex; align-items: center; justify-content: space-between; }
    .completada span { text-decoration: line-through; color: #999; }
    .acciones { display: flex; gap: 0.4rem; }
    .empty { color: #999; font-size: 0.9rem; text-align: center; padding: 2rem; }
  </style>
</head>
<body>
  <h1>Lista de tareas <small style="font-size:0.9rem;color:#888;">({{ total }} total)</small></h1>

  <form method="post" action="/nueva/">
    <input type="text" name="titulo" placeholder="Nueva tarea..." required autofocus>
    <button class="btn-add" type="submit">Agregar</button>
  </form>

  {% if tareas %}
    <ul>
      {% for t in tareas %}
        <li class="{% if t.completada %}completada{% endif %}">
          <span>{{ t.titulo }}</span>
          <div class="acciones">
            <form method="post" action="/completar/{{ t.id }}/" style="display:inline">
              <button class="btn-done" type="submit">{% if t.completada %}↩{% else %}✓{% endif %}</button>
            </form>
            <form method="post" action="/eliminar/{{ t.id }}/" style="display:inline">
              <button class="btn-del" type="submit">✕</button>
            </form>
          </div>
        </li>
      {% endfor %}
    </ul>
  {% else %}
    <p class="empty">No hay tareas. ¡Agregá una arriba!</p>
  {% endif %}
</body>
</html>
"""

# ─── Vistas ──────────────────────────────────────────────────────────────────

def lista(request):
    template = Template(HTML)
    ctx = Context({"tareas": tareas, "total": len(tareas)})
    return HttpResponse(template.render(ctx))


def nueva(request):
    global contador
    titulo = request.POST.get("titulo", "").strip()
    if titulo:
        contador += 1
        tareas.append({"id": contador, "titulo": titulo, "completada": False})
    return HttpResponseRedirect("/")


def completar(request, tarea_id):
    for t in tareas:
        if t["id"] == tarea_id:
            t["completada"] = not t["completada"]
            break
    return HttpResponseRedirect("/")


def eliminar(request, tarea_id):
    tareas[:] = [t for t in tareas if t["id"] != tarea_id]
    return HttpResponseRedirect("/")


# ─── URLs ────────────────────────────────────────────────────────────────────

urlpatterns = [
    path("",                   lista),
    path("nueva/",             nueva),
    path("completar/<int:tarea_id>/", completar),
    path("eliminar/<int:tarea_id>/",  eliminar),
]

# ─── Arranque ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "")
    execute_from_command_line(sys.argv)