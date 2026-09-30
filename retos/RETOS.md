# Evaluación de Web Scraping — ModaLínea

**Objetivo:** extraer información de una tienda de ropa en línea (ficticia) y generar los archivos que servirán como evidencia para un informe de pentesting.

**Herramientas permitidas:** `requests`, `BeautifulSoup`, `lxml` + XPath, `Scrapy`.

## Preparación

```bash
python generar_sitio.py
python -m http.server 8000 --directory sitio
# Abrir http://localhost:8000
```

> ⚠️ Trabaja **solo** contra `http://localhost:8000`. Todo el contenido (correos, claves, credenciales) es ficticio. En un pentesting real necesitas autorización escrita del propietario del sistema.

Antes de programar, explora el sitio con el navegador (F12 → Elements / Network) e identifica la estructura de las páginas.

---

## Reto 1 — Scraping horizontal (30 pts) · `requests` + `BeautifulSoup`

Recorrer **todas las páginas del catálogo** (mismo nivel) y obtener el inventario completo.

**Requisitos**
- No escribir el número de páginas a mano: el script debe detenerse solo cuando ya no exista el botón «Siguiente».
- Precios como número (`1299.0`, no `"$1,299.00 MXN"`).
- Detectar si el producto está agotado y si tiene descuento.

**Entregable:** `productos.csv` con las columnas
`sku, nombre, categoria, precio, precio_antes, agotado, url`

**Preguntas para el informe:** ¿cuántos productos hay? ¿cuántos tienen descuento? ¿cuántos están agotados? ¿precio promedio por categoría?

---

## Reto 2 — Scraping vertical (30 pts) · `lxml` + XPath

Partir de las URLs de `productos.csv` y **descender a la ficha de cada producto** (nivel inferior) para extraer datos que no aparecen en el listado.

**Requisitos**
- Usar **XPath** (no selectores CSS).
- Manejar productos sin reseñas y productos agotados sin romper el script.

**Entregable:** `detalle_productos.json`; por producto:
`sku, url, tallas (lista), material, color, stock (int), num_resenas, promedio_estrellas, resenas (lista de {autor, estrellas, texto})`

**Preguntas para el informe:** ¿qué productos no tienen reseñas? ¿cuál tiene el mejor promedio? ¿qué talla es la más frecuente?

---

## Reto 3 — Horizontal + vertical y hallazgos de seguridad (40 pts) · `Scrapy`

Construir un **spider** que rastree todo el sitio (catálogo y fichas) y, además, recolecte información sensible expuesta.

**Debe recolectar**
1. Comentarios HTML con información sospechosa (credenciales, entornos de prueba, contactos).
2. Correos electrónicos encontrados.
3. Campos `<input type="hidden">` con valores.
4. Rutas declaradas en `robots.txt` (`Disallow`) y su **código de estado** al visitarlas.

**Requisitos**
- Un solo spider, salida con `-O hallazgos.json`.
- Cada registro con al menos: `tipo`, `url`, `contenido`.
- Filtrar el ruido (comentarios inofensivos) y **eliminar duplicados** al preparar el informe.

**Entregables:** `hallazgos.json` y `informe.md` con una tabla:

| # | Hallazgo | URL | Severidad (Alta/Media/Baja) | Recomendación |
|---|----------|-----|-----------------------------|---------------|

---

## Rúbrica

| Criterio | Puntos |
|----------|--------|
| Archivos generados correctos y completos | 40 |
| Uso adecuado de la herramienta pedida en cada reto | 25 |
| Robustez (paginación dinámica, datos faltantes, limpieza) | 15 |
| Informe: hallazgos, severidad y recomendaciones | 20 |
