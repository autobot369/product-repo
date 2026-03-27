/**
 * Mermaid Lightbox — attaches GLightbox to rendered Mermaid diagrams.
 *
 * After Mermaid renders each SVG, this script:
 *  1. Serialises the SVG to a data URL
 *  2. Wraps the diagram container in a clickable overlay with a zoom hint
 *  3. Opens GLightbox programmatically on click so the diagram is viewable full-screen
 */

function attachMermaidLightbox() {
  document.querySelectorAll(".mermaid").forEach(function (container) {
    if (container.dataset.lightboxReady) return;

    const svg = container.querySelector("svg");
    if (!svg) return;

    container.dataset.lightboxReady = "true";
    container.style.cursor = "zoom-in";
    container.title = "Click to view full screen";

    // Add a subtle expand hint badge
    const hint = document.createElement("div");
    hint.textContent = "⛶  full screen";
    hint.style.cssText = [
      "position:absolute",
      "bottom:8px",
      "right:10px",
      "font-size:11px",
      "color:var(--md-default-fg-color--light, #888)",
      "pointer-events:none",
      "opacity:0.7",
    ].join(";");
    container.style.position = "relative";
    container.appendChild(hint);

    container.addEventListener("click", function () {
      // Re-serialise on each click so the latest render is used
      const currentSvg = container.querySelector("svg");
      if (!currentSvg) return;

      const svgString = new XMLSerializer().serializeToString(currentSvg);
      const dataUrl =
        "data:image/svg+xml;charset=utf-8," + encodeURIComponent(svgString);

      const lightbox = GLightbox({
        elements: [
          {
            href: dataUrl,
            type: "image",
            description: container.closest("details")
              ? container.closest("details").querySelector("summary")?.textContent?.trim() || "Diagram"
              : "Diagram",
          },
        ],
        zoomable: true,
        draggable: false,
        touchNavigation: false,
        closeButton: true,
        keyboardNavigation: false,
      });

      lightbox.open();
    });
  });
}

// Run after each MkDocs page navigation (Material theme SPA)
if (typeof document$ !== "undefined") {
  document$.subscribe(function () {
    // Mermaid renders asynchronously — poll until SVGs appear
    let attempts = 0;
    const poll = setInterval(function () {
      const pending = document.querySelectorAll(".mermaid:not([data-lightbox-ready])");
      const hasSvg = Array.from(pending).some(function (el) {
        return el.querySelector("svg");
      });

      if (hasSvg || attempts > 20) {
        clearInterval(poll);
        attachMermaidLightbox();
      }
      attempts++;
    }, 200);
  });
} else {
  // Fallback for non-SPA / direct page load
  document.addEventListener("DOMContentLoaded", function () {
    setTimeout(attachMermaidLightbox, 800);
  });
}
