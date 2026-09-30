#!/usr/bin/env python3
"""
Genera el sitio de práctica "ModaLínea" (tienda de ropa ficticia) en ./sitio
Uso:
    python generar_sitio.py
    python -m http.server 8000 --directory sitio
Luego abrir http://localhost:8000
Todo el contenido (marcas, correos, credenciales, claves) es FICTICIO.
"""
import html
import os
import random
import shutil

random.seed(2026)  # mismo sitio siempre: los resultados esperados no cambian

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sitio")
POR_PAGINA = 8
TOTAL = 40

TIPOS = [
    ("Camisa Oxford", "Hombre", 599, 999, "Algodón 100%"),
    ("Playera Básica", "Unisex", 199, 349, "Algodón peinado"),
    ("Jeans Slim", "Hombre", 699, 1199, "Mezclilla stretch"),
    ("Vestido Floral", "Mujer", 799, 1399, "Viscosa"),
    ("Blusa Satinada", "Mujer", 449, 799, "Poliéster satinado"),
    ("Sudadera con Capucha", "Unisex", 649, 1099, "Felpa de algodón"),
    ("Chamarra Bomber", "Hombre", 1199, 1999, "Nylon reciclado"),
    ("Falda Plisada", "Mujer", 499, 899, "Poliéster"),
    ("Pantalón Cargo", "Hombre", 749, 1249, "Gabardina de algodón"),
    ("Abrigo de Lana", "Mujer", 1799, 2999, "Lana 60% / Poliéster 40%"),
]
COLORES = ["Negro", "Blanco", "Azul Marino", "Rojo", "Verde Oliva", "Beige", "Gris", "Mostaza"]
TALLAS = ["XS", "S", "M", "L", "XL"]
AUTORES = ["Ana", "Luis", "Carla", "Miguel", "Sofía", "Diego", "Valeria", "Jorge"]
TEXTOS = [
    "Muy buena calidad, llegó rápido.",
    "La talla corre un poco chica.",
    "Me encantó el color, tal como en la foto.",
    "Cómoda, pero la tela arruga fácil.",
    "Excelente relación calidad-precio.",
    "No quedó como esperaba, pero el envío fue bueno.",
]


def dinero(x):
    return f"${x:,.2f}"


def generar_productos():
    productos = []
    for i in range(TOTAL):
        nombre_base, cat, pmin, pmax, material = TIPOS[i % len(TIPOS)]
        color = COLORES[(i * 3 + i // len(TIPOS)) % len(COLORES)]
        precio = random.randrange(pmin, pmax, 10) + 9
        precio_antes = round(precio * 1.25 / 10) * 10 + 9 if random.random() < 0.35 else None
        stock = 0 if random.random() < 0.15 else random.choice([3, 8, 15, 42])
        tallas = sorted(random.sample(TALLAS, random.randint(2, 5)), key=TALLAS.index)
        resenas = [
            {
                "autor": random.choice(AUTORES),
                "estrellas": random.randint(2, 5),
                "texto": random.choice(TEXTOS),
            }
            for _ in range(random.randint(0, 3))
        ]
        productos.append(
            {
                "sku": f"MOD-{1000 + i}",
                "nombre": f"{nombre_base} {color}",
                "categoria": cat,
                "color": color,
                "material": material,
                "precio": precio,
                "precio_antes": precio_antes,
                "stock": stock,
                "tallas": tallas,
                "resenas": resenas,
            }
        )
    return productos


CSS = """
:root{--c1:#1f2a44;--c2:#e07a5f;--bg:#f7f5f2;--t:#222}
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,Segoe UI,Arial,sans-serif;background:var(--bg);color:var(--t)}
header{background:var(--c1);color:#fff;padding:14px 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
header a{color:#fff;text-decoration:none;margin-right:16px}
header .logo{font-size:1.4rem;font-weight:700}
main{max-width:1100px;margin:24px auto;padding:0 16px}
.breadcrumb{font-size:.85rem;color:#666;margin-bottom:12px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px}
.producto{background:#fff;border-radius:10px;padding:12px;box-shadow:0 1px 4px #0002;position:relative}
.producto img,.detalle img{width:100%;background:#eee;border-radius:8px}
.producto h2{font-size:1rem;margin:8px 0 4px}
.categoria{color:#777;font-size:.8rem;margin:0}
.precio-actual{font-weight:700;color:var(--c1)}
.precio-antes{text-decoration:line-through;color:#999;margin-left:8px;font-size:.9rem}
.etiqueta-agotado{position:absolute;top:8px;right:8px;background:#b00020;color:#fff;font-size:.75rem;padding:3px 8px;border-radius:12px}
.paginacion{display:flex;gap:8px;justify-content:center;margin:28px 0;flex-wrap:wrap}
.paginacion a,.paginacion span{padding:6px 12px;background:#fff;border-radius:6px;text-decoration:none;color:var(--c1);box-shadow:0 1px 3px #0002}
.paginacion .actual{background:var(--c2);color:#fff}
.detalle{display:grid;grid-template-columns:1fr 1fr;gap:24px;background:#fff;padding:20px;border-radius:10px}
@media(max-width:700px){.detalle{grid-template-columns:1fr}}
ul.tallas{list-style:none;padding:0;display:flex;gap:8px}
ul.tallas li{border:1px solid var(--c1);border-radius:6px;padding:4px 10px}
table.especificaciones{border-collapse:collapse;width:100%}
table.especificaciones td,table.especificaciones th{border-bottom:1px solid #ddd;padding:6px;text-align:left}
.resena{border-top:1px solid #ddd;padding:8px 0}
footer{background:var(--c1);color:#ccc;padding:20px 24px;margin-top:40px;font-size:.9rem}
footer input,footer button{padding:6px}
"""

PLACEHOLDER_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300"><rect width="300" height="300" fill="#e8e4df"/><path d="M90 70l40-20q20 25 40 0l40 20 40 50-40 20v110H90V140L50 120z" fill="#b8b0a6"/></svg>"""


def layout(titulo, cuerpo, prefijo, extra_footer=""):
    """prefijo: ruta relativa a la raíz ('' , '../')"""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titulo)} | ModaLínea</title>
<link rel="stylesheet" href="{prefijo}css/style.css">
</head>
<body>
<!-- Encabezado principal -->
<header>
  <a class="logo" href="{prefijo}index.html">ModaLínea</a>
  <nav>
    <a href="{prefijo}catalogo/pagina-1.html">Catálogo</a>
    <a href="{prefijo}index.html#ofertas">Ofertas</a>
    <a href="mailto:soporte@modalinea.test">Contacto</a>
  </nav>
</header>
<main>
{cuerpo}
</main>
<footer>
  <p>© 2026 ModaLínea (sitio ficticio para prácticas de scraping).</p>
  <form action="#" method="post">
    <input type="email" name="correo" placeholder="Tu correo">
    <button type="button">Suscribirme</button>
    {extra_footer}
  </form>
</footer>
</body>
</html>
"""


def tarjeta(p):
    antes = f'<span class="precio-antes">{dinero(p["precio_antes"])} MXN</span>' if p["precio_antes"] else ""
    agotado = '<span class="etiqueta-agotado">Agotado</span>' if p["stock"] == 0 else ""
    return f"""    <article class="producto" data-sku="{p['sku']}">
      {agotado}
      <a class="enlace-producto" href="../producto/{p['sku']}.html">
        <img src="../img/prenda.svg" alt="{html.escape(p['nombre'])}" width="300" height="300">
        <h2 class="nombre">{html.escape(p['nombre'])}</h2>
      </a>
      <p class="categoria">{p['categoria']}</p>
      <div class="precios"><span class="precio-actual">{dinero(p['precio'])} MXN</span>{antes}</div>
    </article>"""


def pagina_catalogo(n, total_paginas, items):
    tarjetas = "\n".join(tarjeta(p) for p in items)
    nums = []
    for i in range(1, total_paginas + 1):
        if i == n:
            nums.append(f'<span class="actual">{i}</span>')
        else:
            nums.append(f'<a href="pagina-{i}.html">{i}</a>')
    ant = f'<a class="anterior" rel="prev" href="pagina-{n-1}.html">« Anterior</a>' if n > 1 else ""
    sig = f'<a class="siguiente" rel="next" href="pagina-{n+1}.html">Siguiente »</a>' if n < total_paginas else ""
    comentario = ""
    if n == 3:
        comentario = "<!-- TODO: quitar antes de produccion. Probar cambios en https://staging.modalinea.test/catalogo -->\n"
    cuerpo = f"""<div class="breadcrumb">Inicio › Catálogo › Página {n}</div>
<h1>Catálogo de prendas</h1>
{comentario}<section id="catalogo" class="grid">
{tarjetas}
</section>
<nav class="paginacion">
  {ant}
  {' '.join(nums)}
  {sig}
</nav>"""
    return layout(f"Catálogo - página {n}", cuerpo, "../")


def pagina_producto(p):
    antes = f'<span class="precio-antes">{dinero(p["precio_antes"])} MXN</span>' if p["precio_antes"] else ""
    tallas = "\n".join(f'      <li class="talla">{t}</li>' for t in p["tallas"])
    stock = (
        '<p class="stock agotado">Agotado</p>'
        if p["stock"] == 0
        else f'<p class="stock">Disponibles: {p["stock"]} piezas</p>'
    )
    if p["resenas"]:
        resenas = "\n".join(
            f"""    <div class="resena">
      <span class="autor">{r['autor']}</span>
      <span class="estrellas" data-valor="{r['estrellas']}">{'★' * r['estrellas']}{'☆' * (5 - r['estrellas'])}</span>
      <p class="texto">{html.escape(r['texto'])}</p>
    </div>"""
            for r in p["resenas"]
        )
    else:
        resenas = '    <p class="sin-resenas">Aún no hay reseñas.</p>'
    comentario = ""
    if p["sku"] == "MOD-1013":
        comentario = "<!-- Contacto dev: dev.tienda@modalinea.test | usuario: admin | pass temporal: Cambiar123 -->\n"
    cuerpo = f"""<div class="breadcrumb">Inicio › Catálogo › {p['categoria']} › {html.escape(p['nombre'])}</div>
{comentario}<section class="detalle">
  <img src="../img/prenda.svg" alt="{html.escape(p['nombre'])}">
  <div>
    <h1 class="nombre">{html.escape(p['nombre'])}</h1>
    <p class="sku">SKU: {p['sku']}</p>
    <p class="precios"><span class="precio-actual">{dinero(p['precio'])} MXN</span>{antes}</p>
    {stock}
    <h3>Tallas disponibles</h3>
    <ul class="tallas">
{tallas}
    </ul>
    <h3>Especificaciones</h3>
    <table class="especificaciones">
      <tr><th>Material</th><td>{html.escape(p['material'])}</td></tr>
      <tr><th>Categoría</th><td>{p['categoria']}</td></tr>
      <tr><th>Color</th><td>{p['color']}</td></tr>
      <tr><th>Cuidado</th><td>Lavar a máquina en agua fría</td></tr>
    </table>
  </div>
</section>
<section id="resenas">
  <h2>Reseñas de clientes</h2>
{resenas}
</section>
<p><a href="../catalogo/pagina-1.html">« Volver al catálogo</a></p>"""
    return layout(p["nombre"], cuerpo, "../")


def escribir(ruta, contenido):
    ruta = os.path.join(SALIDA, ruta)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)


def main():
    if os.path.exists(SALIDA):
        shutil.rmtree(SALIDA)
    productos = generar_productos()
    total_paginas = (len(productos) + POR_PAGINA - 1) // POR_PAGINA

    escribir("css/style.css", CSS)
    escribir("img/prenda.svg", PLACEHOLDER_SVG)

    # Portada
    destacados = productos[:4]
    dest_html = "\n".join(
        f'    <li><a href="producto/{p["sku"]}.html">{html.escape(p["nombre"])}</a></li>' for p in destacados
    )
    portada = f"""<h1>Bienvenido a ModaLínea</h1>
<p>Ropa para toda la familia, directo a tu puerta.</p>
<section id="ofertas">
  <h2>Destacados</h2>
  <ul>
{dest_html}
  </ul>
  <p><a href="catalogo/pagina-1.html">Ver todo el catálogo »</a></p>
</section>"""
    extra = '<input type="hidden" name="api_key" value="FAKE-KEY-9f8e7d6c5b4a">\n    <input type="hidden" name="campana" value="otono2026">'
    escribir("index.html", layout("Inicio", portada, "", extra))

    # Catálogo paginado
    for n in range(1, total_paginas + 1):
        items = productos[(n - 1) * POR_PAGINA : n * POR_PAGINA]
        escribir(f"catalogo/pagina-{n}.html", pagina_catalogo(n, total_paginas, items))

    # Fichas
    for p in productos:
        escribir(f"producto/{p['sku']}.html", pagina_producto(p))

    # Superficie "olvidada" para el informe de pentesting
    escribir(
        "robots.txt",
        "User-agent: *\nDisallow: /admin/\nDisallow: /backup/\nDisallow: /api/interno/\nAllow: /\n",
    )
    escribir(
        "admin/index.html",
        layout(
            "Panel de administración",
            '<h1>Acceso administrativo</h1>\n<form method="post" action="#">\n'
            '<input name="usuario" placeholder="usuario"> <input type="password" name="clave">\n'
            '<button type="button">Entrar</button>\n</form>',
            "../",
        ),
    )
    escribir(
        "backup/index.html",
        layout(
            "Index of /backup",
            "<h1>Index of /backup</h1>\n<ul>\n<li><a href=\"tienda_2026.sql.txt\">tienda_2026.sql.txt</a></li>\n</ul>",
            "../",
        ),
    )
    escribir("backup/tienda_2026.sql.txt", "-- Respaldo ficticio\n-- contacto: dba@modalinea.test\nCREATE TABLE clientes (id INT, correo TEXT);\n")

    agotados = sum(1 for p in productos if p["stock"] == 0)
    descuento = sum(1 for p in productos if p["precio_antes"])
    sin_resenas = sum(1 for p in productos if not p["resenas"])
    print(f"Sitio generado en: {SALIDA}")
    print(f"  Productos: {len(productos)} en {total_paginas} páginas")
    print(f"  Agotados: {agotados} | Con descuento: {descuento} | Sin reseñas: {sin_resenas}")


if __name__ == "__main__":
    main()
