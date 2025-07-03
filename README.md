# MangaPlus Selenium Scraper

Este proyecto es un scraper automatizado para descargar capítulos de manga desde [manhuaplus.com](https://manhuaplus.com) y guardarlos como archivos PDF, usando Python, Selenium y Pillow.

---

## ¿Qué hace este script?

- **Navega automáticamente** por la página de un manga en manhuaplus.com.
- **Extrae la lista de capítulos** disponibles.
- **Abre cada capítulo** en un navegador Firefox controlado por Selenium.
- **Hace scroll automático** para cargar todas las imágenes del capítulo.
- **Descarga todas las imágenes** de cada capítulo.
- **Genera un PDF** por cada capítulo, guardando el archivo en una carpeta con el nombre del manga y el capítulo.
- **Elimina las imágenes temporales** después de crear el PDF.

---

## Requisitos

- Python 3.8+
- [Selenium](https://pypi.org/project/selenium/)
- [Pillow](https://pypi.org/project/Pillow/)
- [requests](https://pypi.org/project/requests/)
- Firefox instalado
- [geckodriver](https://github.com/mozilla/geckodriver/releases) instalado y accesible en tu PATH

Instala las dependencias con:
```bash
pip install selenium pillow requests
```

En Ubuntu puedes instalar Firefox y geckodriver con:
```bash
sudo apt update
sudo apt install firefox firefox-geckodriver
```

---

## Uso rápido

1. **Configura la URL del manga**
   - Edita la variable `BASE_URL` en `main.py` y pon la URL del manga que quieres descargar.

2. **Ejecuta el script**
   ```bash
   python main.py
   ```

3. **Resultados**
   - Se creará una carpeta `output/`.
   - Dentro de `output/` habrá una subcarpeta por cada capítulo, con el nombre del manga y el capítulo.
   - Dentro de cada subcarpeta estará el PDF del capítulo.

---

## Explicación técnica (para programadores)

- **Selenium** se usa para abrir Firefox en modo headless y navegar por la web como un usuario real.
- El script extrae los enlaces de capítulos usando selectores CSS.
- Para cada capítulo:
  - Abre la página del capítulo.
  - Espera a que las imágenes estén presentes.
  - Hace scroll sobre el contenedor `.reading-content` para cargar imágenes lazy-load.
  - Extrae todas las URLs de imágenes (`<img src=...>`), convirtiendo URLs relativas a absolutas.
  - Descarga cada imagen usando `requests` con headers personalizados para evitar bloqueos.
  - Guarda las imágenes en una carpeta temporal específica del capítulo.
  - Usa Pillow para convertir las imágenes a un PDF.
  - Elimina las imágenes temporales tras crear el PDF.
- El nombre del PDF y la carpeta se genera a partir del nombre del manga y el capítulo, extraídos de la URL.

---

## Explicación no técnica (para usuarios)

- Este programa "simula" a una persona navegando por la web del manga.
- Va capítulo por capítulo, abre la página, baja hasta el final para que se carguen todas las imágenes, y las descarga.
- Junta todas las imágenes de cada capítulo en un solo archivo PDF, para que puedas leer el manga offline.
- Todo se guarda ordenado en carpetas, y no necesitas hacer nada manualmente más que ejecutar el script.

---

## Notas y recomendaciones

- El script puede tardar dependiendo de la cantidad de capítulos y la velocidad de tu conexión.
- Si el sitio cambia su estructura HTML, puede que necesites actualizar los selectores en el script.
- No abuses del scraping: respeta los tiempos de espera y no descargues cientos de capítulos en poco tiempo.
- Este script es solo para uso personal y educativo.

---

## ¿Preguntas o problemas?

Si tienes dudas o el script deja de funcionar, revisa los mensajes de error en consola y asegúrate de que:
- Tienes Firefox y geckodriver instalados.
- La URL del manga es correcta.
- El sitio no ha cambiado su estructura.

Puedes abrir un issue o pedir ayuda si necesitas soporte adicional. 