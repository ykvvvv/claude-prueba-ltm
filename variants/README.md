# Variantes de diseño — LTM Partners

Tres rediseños de https://ltmpartners.site con **el mismo contenido**. No se tocó el sitio original (este repo no lo contiene; el contenido se leyó de la web en vivo el 2026-11-16).

## Cómo abrirlas
Doble clic en `variante-a.html`, `variante-b.html` o `variante-c.html`. Se abren en el navegador; necesitan internet para cargar fuentes, logos y fotos.

## Qué cambia en cada una

| | A · Terminal | B · Editorial (recomendada) | C · Bento |
|---|---|---|---|
| Acento | Verde menta `#5FE3B1` | Dorado `#D9B65A` (el dorado actual de la marca) | Azul eléctrico `#4C8DFF` |
| Tipografía | Inter + IBM Plex Mono para cifras y etiquetas | Instrument Serif (títulos) + Inter | Manrope |
| Hero | Texto + panel de mercados tipo tabla | Titular enorme que se revela línea por línea | Cuadrícula bento con los contadores dentro |
| Cifras | Contador tipo ticker (se pinta del acento mientras cuenta) | Números grandes en serif | Tarjetas del bento |
| Servicios/Modelos | Tabla de líneas finas, bordes que se iluminan al pasar el cursor | Lista editorial a dos columnas | Bento con resplandor que sigue al cursor |
| Creadores | Fila de 4 tarjetas | Fotos grandes sin tarjeta | Bento (1 grande + 3) |

## Común a las tres
- Secciones: Hero, Marcas (carrusel), Cifras, Modelos CPA/FTD, Servicios, Metodología, Creadores, GEOs (7 pestañas con datos), Contacto, Formulario de postulación y Footer.
- Animaciones: aparición al hacer scroll (IntersectionObserver), contadores de 0 al valor real y carrusel de marcas. Solo usan `transform` y `opacity` con curvas ease-out de 200 a 400 ms. Excepciones: los contadores duran ~1,1 s para que se alcancen a leer, y el titular de B dura 0,9 s.
- `prefers-reduced-motion`: sin animaciones; los contadores muestran el valor final y el carrusel queda como una grilla fija.
- Sin JS el contenido se ve igual (los contadores traen el valor real en el HTML).
- Pestañas de GEOs accesibles con teclado (flechas, Inicio, Fin). Hay enlace "Saltar al contenido" y foco visible.
- Sin Tailwind, Lucide, Calendly ni otras librerías: solo Google Fonts. Los íconos son SVG en línea.

## Correcciones respecto al sitio actual
1. **Contadores en 0**: ahora el valor real viene en el HTML y la animación solo parte desde 0 si el usuario permite movimiento.
2. **Metodología faltante**: el menú apuntaba a `#metodologia`, que no existía. Se creó la sección con 4 pasos tomados de los servicios actuales. **Revísala: es una propuesta.**
3. **"Conviértete en afiliado"**: ahora lleva a `#postular`, un formulario visible en la página. El enlace `#creadores-form` no existía.
4. **Textos en inglés** traducidos: "GENERATING HIGH-IMPACT TRAFFIC…", Followers/Views, High Engagement, Avg FTD, los niveles de cada GEO, etc. Se mantienen términos del rubro como CPA, FTD, IRL, Slots y Tier 1.
5. **Footer**: aviso +18 y texto de juego responsable.
6. **Formulario**: valida campos, pide confirmar mayoría de edad y abre el correo con asunto y cuerpo armados. Antes usaba `mailto` con POST, que muchos navegadores no manejan bien.
7. **Calendly**: ahora es un enlace que abre en una pestaña nueva, en vez de un widget embebido.
8. Se quitó el globo 3D: era un canvas animado sin pausa. Lo reemplaza una lista de mercados.

## [COMPLETAR] y datos para verificar (no se inventó nada)
- Tarifas y condiciones de CPA y FTD por GEO.
- Plazos de la metodología y frecuencia de los reportes.
- Línea de ayuda de juego responsable por país.
- **4 creadores de GEOs sin enlace ni foto** en el sitio original: Diego "ElPeru", Camilo Parra, Rodrigo "ElAzteca" e IberianBets ES. Confirma que existan antes de publicar.
- La foto `images/juan.jpg` da 404 en el sitio en vivo. Las variantes muestran sus iniciales.
- Cifras que no cuadran (vienen del sitio, no se cambiaron):
  - "4 GEOs clave activos" vs. 7 pestañas.
  - La suma de creadores por país (445+) supera "200+".
  - En Global, "FTD promedio" es "$85+ USD" mientras en el resto es un %.
  - "Bynico +750 vistas" parece bajo.

## Notas técnicas
- Fotos y páginas legales apuntan a URLs absolutas de `ltmpartners.site` para que funcionen al abrir el archivo localmente. Al publicar se pueden volver relativas.
- `_fuente/build.py` genera las tres variantes desde un solo bloque de contenido: `python3 variants/_fuente/build.py variants`. **Si editas un HTML a mano, no lo regeneres, porque perderías esos cambios.**
