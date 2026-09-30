# Práctica de Web Scraping — ModaLínea

Evaluación práctica de web scraping sobre una tienda de ropa **ficticia**, ejecutada en tu propia máquina.
Herramientas: `requests`, `BeautifulSoup`, `lxml` + XPath y `Scrapy`.

## Inicio rápido

```bash
git clone <URL-DEL-REPOSITORIO>
cd scraping-modalinea-alumnos

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python generar_sitio.py                      # crea la carpeta sitio/
python -m http.server 8000 --directory sitio # déjalo corriendo en una terminal
```

Abre <http://localhost:8000> en el navegador y explora la tienda antes de programar.

## Retos

El enunciado completo, los entregables y la rúbrica están en **[retos/RETOS.md](retos/RETOS.md)**.

| Reto | Tipo | Herramienta | Entregable |
|------|------|-------------|------------|
| 1 | Horizontal (paginación) | requests + BeautifulSoup | `productos.csv` |
| 2 | Vertical (fichas de producto) | lxml + XPath | `detalle_productos.json` |
| 3 | Horizontal + vertical + hallazgos | Scrapy | `hallazgos.json` + `informe.md` |

Guarda tus scripts en una carpeta `entrega/` (crea una rama o un fork; no modifiques `generar_sitio.py`).

## Aviso ético

Trabaja **únicamente** contra `http://localhost:8000`. Todo el contenido (correos, claves, credenciales) es ficticio.
En un pentesting real necesitas autorización escrita del propietario del sistema.
