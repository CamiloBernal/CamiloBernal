import os

def generate_header_svg(text, filename, width=800, height=60):
    """
    Generates a custom SVG header with a gradient.
    """
    svg_content = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#8B5CF6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#00D9FF;stop-opacity:1" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"
        font-family="'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
        font-size="30" font-weight="bold" fill="url(#gradient)" filter="url(#glow)">
    {text}
  </text>
</svg>
"""
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Generated SVG: {filename}")
    except Exception as e:
        print(f"Error generating SVG {filename}: {e}")

if __name__ == "__main__":
    # Example usage
    headers = {
        "about": "⚡ Sobre Mí",
        "metrics": "📊 Métricas en Tiempo Real",
        "stack": "🛠️ Arsenal Tecnológico",
        "projects": "🚀 Proyectos Destacados",
        "activity": "📡 Actividad Reciente",
        "connect": "🤝 Conectemos"
    }

    for key, text in headers.items():
        generate_header_svg(text, f"src/assets/headers/{key}.svg")
