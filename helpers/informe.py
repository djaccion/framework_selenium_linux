"""Informe HTML de un caso, con la captura de cada paso.

Autocontenido a propósito: las imágenes van embebidas, así que el archivo se puede
adjuntar a un ticket, mandar por correo o publicar como artefacto del pipeline sin
arrastrar la carpeta de evidencias.
"""
import base64
import html
import os
from datetime import datetime

COLORES = {
    "passed": ("#059669", "#ecfdf5", "#a7f3d0", "exitoso"),
    "failed": ("#dc2626", "#fef2f2", "#fecaca", "fallido"),
    "error": ("#dc2626", "#fef2f2", "#fecaca", "error"),
    "skipped": ("#7c3aed", "#f5f3ff", "#ddd6fe", "omitido"),
}

ICONO = {"navegar": "→", "clic": "✔", "escribir": "⌨", "fallo": "✖"}


def _esc(t):
    return html.escape(str(t if t is not None else ""))


def _imagen(ruta):
    try:
        with open(ruta, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""


def escribir(caso, estado, duracion_s, pasos, carpeta="reportes", detalle_fallo=""):
    """Genera el informe y devuelve su ruta."""
    color, fondo, borde, rotulo = COLORES.get(estado, ("#475569", "#f8fafc", "#e2e8f0", estado))

    tarjetas = []
    for p in pasos:
        img = _imagen(p.get("archivo", ""))
        falla = p.get("accion") == "fallo"
        tarjetas.append(
            '<figure class="paso%s">'
            '<figcaption><span class="n">%s</span>'
            '<span class="acc">%s %s</span>'
            '<span class="det">%s</span></figcaption>%s'
            '<div class="url">%s</div></figure>' % (
                " falla" if falla else "",
                p.get("n"), ICONO.get(p.get("accion"), "•"), _esc(p.get("accion")),
                _esc(p.get("detalle")),
                ('<a href="data:image/png;base64,%s" target="_blank">'
                 '<img src="data:image/png;base64,%s" alt="paso %s"></a>'
                 % (img, img, p.get("n"))) if img else '<div class="sinimg">sin captura</div>',
                _esc(p.get("url"))))

    if not tarjetas:
        tarjetas = ['<p class="vacio">Sin pasos registrados. '
                    'Comprobá que <code>AUTOMATION_PASOS</code> no esté en <code>false</code>.</p>']

    cuerpo = """<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(caso)s · %(rotulo)s</title>
<style>
 * { box-sizing:border-box; }
 body { margin:0; font:15px/1.55 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
        color:#0f172a; background:#f1f5f9; }
 header { background:#0f172a; color:#fff; padding:26px 32px; }
 header h1 { margin:0 0 4px; font-size:20px; font-weight:700; }
 header .sub { color:#94a3b8; font-size:13px; }
 .cinta { display:flex; flex-wrap:wrap; background:#fff; border-bottom:1px solid #e2e8f0; }
 .dato { padding:14px 24px; border-right:1px solid #e2e8f0; }
 .dato .k { font-size:11px; text-transform:uppercase; letter-spacing:.06em; color:#64748b; }
 .dato .v { font-size:17px; font-weight:700; margin-top:2px; }
 .chip { display:inline-block; padding:3px 12px; border-radius:999px; font-weight:700;
         font-size:13px; color:%(color)s; background:%(fondo)s; border:1px solid %(borde)s; }
 main { padding:24px 32px 60px; max-width:1400px; margin:0 auto; }
 h2 { font-size:14px; text-transform:uppercase; letter-spacing:.06em; color:#475569; margin:28px 0 12px; }
 .pasos { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:16px; }
 .paso { margin:0; background:#fff; border:1px solid #e2e8f0; border-radius:12px; overflow:hidden;
         box-shadow:0 1px 2px rgba(15,23,42,.05); }
 .paso.falla { border-color:#fecaca; box-shadow:0 0 0 2px #fee2e2; }
 .paso figcaption { padding:10px 12px; border-bottom:1px solid #f1f5f9; }
 .paso .n { display:inline-block; min-width:22px; height:22px; line-height:22px; text-align:center;
            background:#0f172a; color:#fff; border-radius:6px; font-size:11px; font-weight:700; margin-right:8px; }
 .paso .acc { font-weight:600; font-size:13px; }
 .paso .det { display:block; color:#475569; font-size:12px; margin-top:4px; overflow-wrap:anywhere; }
 .paso img { display:block; width:100%%; border-top:1px solid #f1f5f9; }
 .paso .url { padding:8px 12px; font:11px/1.4 ui-monospace,Menlo,Consolas,monospace;
              color:#64748b; background:#f8fafc; overflow-wrap:anywhere; }
 .sinimg { padding:36px; text-align:center; color:#94a3b8; font-size:13px; }
 .vacio { background:#fff; border:1px dashed #cbd5e1; border-radius:12px; padding:24px; color:#64748b; }
 pre { margin:0; padding:14px; background:#0f172a; color:#e2e8f0; border-radius:8px;
       font:12px/1.5 ui-monospace,Menlo,Consolas,monospace; overflow:auto; max-height:420px; }
 footer { padding:18px 32px 40px; color:#94a3b8; font-size:12px; }
 @media print { body { background:#fff; } .paso { break-inside:avoid; } }
</style></head>
<body>
<header><h1>%(caso)s</h1><div class="sub">%(fecha)s</div></header>
<div class="cinta">
  <div class="dato"><div class="k">Resultado</div><div class="v"><span class="chip">%(rotulo)s</span></div></div>
  <div class="dato"><div class="k">Duración</div><div class="v">%(dur)s s</div></div>
  <div class="dato"><div class="k">Pasos</div><div class="v">%(npasos)s</div></div>
</div>
<main>
  <h2>Paso a paso</h2>
  <div class="pasos">%(tarjetas)s</div>
  %(fallo)s
</main>
<footer>Generado por el framework de automatización. Las imágenes van embebidas:
este archivo se puede adjuntar o archivar tal cual.</footer>
</body></html>""" % {
        "caso": _esc(caso),
        "rotulo": _esc(rotulo),
        "color": color, "fondo": fondo, "borde": borde,
        "fecha": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "dur": round(duracion_s or 0, 1),
        "npasos": len(pasos),
        "tarjetas": "".join(tarjetas),
        "fallo": ('<h2>Detalle del fallo</h2><pre>%s</pre>' % _esc(detalle_fallo)
                  if detalle_fallo else ""),
    }

    os.makedirs(carpeta, exist_ok=True)
    limpio = "".join(c if c.isalnum() or c in "-_" else "_" for c in caso)[:80]
    ruta = os.path.join(carpeta, "informe-%s.html" % limpio)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(cuerpo)
    return ruta
