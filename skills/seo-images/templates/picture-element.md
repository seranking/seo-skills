Template `picture-element.html`:

```html
<!-- Below-fold content image: progressive enhancement AVIF → WebP → JPEG fallback -->
<picture>
  <source srcset="{REPLACE: image-400.avif 400w, image-800.avif 800w, image-1200.avif 1200w}"
          sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
          type="image/avif">
  <source srcset="{REPLACE: image-400.webp 400w, image-800.webp 800w, image-1200.webp 1200w}"
          sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
          type="image/webp">
  <img src="{REPLACE: image-800.jpg}"
       srcset="{REPLACE: image-400.jpg 400w, image-800.jpg 800w, image-1200.jpg 1200w}"
       sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
       alt="{REPLACE: descriptive alt text, 10–125 chars}"
       width="{REPLACE: 1200}"
       height="{REPLACE: 800}"
       loading="lazy"
       decoding="async">
</picture>

<!-- LCP / hero image: eager-load, high fetchpriority, NO lazy, NO async-decode -->
<picture>
  <source srcset="{REPLACE: hero-1200.avif 1200w, hero-1920.avif 1920w}"
          sizes="100vw"
          type="image/avif">
  <source srcset="{REPLACE: hero-1200.webp 1200w, hero-1920.webp 1920w}"
          sizes="100vw"
          type="image/webp">
  <img src="{REPLACE: hero-1200.jpg}"
       srcset="{REPLACE: hero-1200.jpg 1200w, hero-1920.jpg 1920w}"
       sizes="100vw"
       alt="{REPLACE: hero alt text}"
       width="{REPLACE: 1920}"
       height="{REPLACE: 1080}"
       fetchpriority="high">
</picture>
```
