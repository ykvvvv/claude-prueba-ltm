# Registro de avances

## 2026-11-16 · Claude Code
**Hecho**
- Leí https://ltmpartners.site (HTML completo) y comprobé imágenes y páginas legales.
- Creé `variante-a.html` (Terminal), `variante-b.html` (Editorial) y `variante-c.html` (Bento). Cada una es autocontenida.
- Apliqué las correcciones listadas en README (contadores, Metodología, enlace de afiliado, traducciones, +18 y juego responsable).

**Verificado (Chromium con Playwright)**
- Sin errores de JS en las 3 variantes, a 360 px y 1440 px.
- Sin scroll horizontal a 360 px.
- Contadores terminan en 200+, 4 y 100%.
- Las pestañas de GEOs cambian el contenido.
- El formulario bloquea el envío con campos vacíos.
- Con reduced-motion no hay animaciones y se ven los valores finales.

**Sin probar**
- Logos de marcas: `i.ibb.co` estaba bloqueado en el entorno de prueba. Si alguno falla, se muestra su nombre en texto.
- Safari/iOS, Firefox, lector de pantalla real y envío real del correo.

**Pendiente**
- Completar los marcadores [COMPLETAR] y resolver las inconsistencias de cifras (ver README).
- Elegir una variante y llevarla al repo real del sitio.
