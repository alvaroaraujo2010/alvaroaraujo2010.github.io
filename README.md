# Sitio personal — Alvaro Araújo (Angular 21)

Landing profesional construida con **Angular 21** para despliegue temporal en Netlify. Incluye CV descargable, imágenes del kit de marketing y perfil extraído del CV 2026.

## Requisitos

- Node.js 20+
- npm 10+

## Desarrollo local

```bash
cd sitio-personal
npm install
npm start
```

Abre `http://localhost:4200`.

## Build de producción

```bash
npm run build
```

Salida: `dist/sitio-personal/browser`

## Despliegue en Netlify

1. Conecta el repositorio o usa **Deploy manually**.
2. **Base directory:** `sitio-personal` (si el repo es la raíz `MARCA`).
3. **Build command:** `npm run build`
4. **Publish directory:** `dist/sitio-personal/browser`

El archivo `netlify.toml` define build, publicación, redirección SPA y **301** desde el dominio antiguo `alvaroaraujoarrieta.tech` hacia `https://alvaro-araujo.netlify.app/`.

### Dominio antiguo → sitio personal

1. En Netlify: **Domain management** → añade `alvaroaraujoarrieta.tech` y `www.alvaroaraujoarrieta.tech` a este mismo sitio.
2. En tu registrador de dominio: apunta el DNS a Netlify (registros A/CNAME que indique el panel).
3. Haz deploy; al visitar el dominio viejo, Netlify redirige al sitio personal.

## Favicon

- `public/assets/images/favicon-source-512.png` — PNG transparente (512×512) para editar o convertir
- `public/assets/images/favicon-source.svg` — fuente vectorial sin fondo
- `public/favicon.ico` — icono multi-tamaño (16–256 px) ya enlazado en `index.html`

## Estructura

- `src/app/core/data/portfolio.data.ts` — datos del CV y rutas de imágenes
- `src/app/pages/home/` — página principal
- `src/app/layout/` — cabecera y pie
- `public/assets/` — CV PDF e imágenes del collage

## Actualizar contenido

Edita `portfolio.data.ts` para experiencia, skills o textos. Sustituye archivos en `public/assets/images/` manteniendo los nombres o actualiza las rutas en `IMAGES`.
