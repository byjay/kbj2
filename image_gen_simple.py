# -*- coding: utf-8 -*-
"""
KBJ2 PPT Image Generator - Free Image APIs

Supports:
- Pollinations.ai (free AI image generation)
- Unsplash Source (free stock photos)
"""

import urllib.request
import urllib.parse
import time
from pathlib import Path
from typing import List, Dict

class ImageGenerator:
    """Free image generation using multiple APIs"""

    def __init__(self, output_dir: str = "F:/kbj2/workspace/images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_image(self, prompt: str, filename: str = None) -> str:
        """
        Generate/download image using free APIs
        Tries multiple sources in order
        """
        if filename is None:
            filename = f"img_{hash(prompt) % 10000}.png"

        filepath = self.output_dir / filename

        # Try Pollinations.ai first (AI generated)
        if not self._try_pollinations(prompt, filepath):
            # Fallback to Unsplash (stock photos)
            self._try_unsplash(prompt, filepath)

        if filepath.exists():
            return str(filepath)
        return ""

    def _try_pollinations(self, prompt: str, filepath: Path) -> bool:
        """Try Pollinations.ai for AI image generation"""
        try:
            encoded = urllib.parse.quote(prompt[:200])  # Limit length
            url = f"https://image.pollinations.ai/prompt/{encoded}"

            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')

            with urllib.request.urlopen(req, timeout=60) as response:
                content = response.read()
                filepath.write_bytes(content)
                print(f"[OK] AI image: {prompt[:40]}")
                return True
        except Exception as e:
            print(f"[WARN] Pollinations: {str(e)[:40]}")
            return False

    def _try_unsplash(self, prompt: str, filepath: Path) -> bool:
        """Try Unsplash for stock photos"""
        try:
            # Extract key words (first 3)
            words = prompt.replace(",", " ").split()[:3]
            search = " ".join(words)

            seed = int(time.time() * 1000) % 10000
            url = f"https://source.unsplash.com/1280x720/?{search}&sig={seed}"

            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')

            with urllib.request.urlopen(req, timeout=60) as response:
                content = response.read()
                filepath.write_bytes(content)
                print(f"[OK] Photo: {search}")
                return True
        except Exception as e:
            print(f"[WARN] Unsplash: {str(e)[:40]}")
            return False

    def generate_batch(self, topics: List[str]) -> Dict[str, str]:
        """Generate images for multiple topics"""
        results = {}

        print(f"\n{'='*50}")
        print(f"[IMAGE GEN] {len(topics)} images")
        print(f"{'='*50}\n")

        for idx, topic in enumerate(topics, 1):
            print(f"[{idx}/{len(topics)}] {topic[:40]}...")

            filename = f"slide_{idx:02d}.png"
            result = self.generate_image(topic, filename)

            if result:
                results[topic] = result

        print(f"\n[DONE] {len(results)}/{len(topics)} generated")
        return results


class PresentationBuilder:
    """Create PPT with images"""

    def __init__(self):
        self.gen = ImageGenerator()
        self.slides_dir = Path("F:/kbj2/workspace/slides")
        self.slides_dir.mkdir(parents=True, exist_ok=True)

    def create_slide_with_image(
        self,
        num: int,
        title: str,
        content: List[str],
        image_path: str = None
    ) -> str:
        """Create HTML slide with embedded image"""
        rel_image = Path(image_path).name if image_path else ""

        html = f"""<!DOCTYPE html>
<html>
<head>
<style>
html {{ background: #ffffff; }}
body {{
  width: 720pt; height: 405pt; margin: 0; padding: 0;
  background: #F4F6F6;
  font-family: Arial, sans-serif;
  display: flex;
}}
.container {{
  display: flex;
  height: 100%;
  margin: 18pt 18pt 35pt 18pt;
  gap: 8pt;
}}
.content {{
  flex: 1;
  background: #FFFFFF;
  border-radius: 8pt;
  padding: 15pt;
}}
.header {{
  border-bottom: 2pt solid #2E4053;
  padding-bottom: 6pt;
  margin-bottom: 10pt;
}}
h1 {{
  color: #1C2833;
  font-size: 18pt;
  margin: 0;
}}
ul {{
  margin: 6pt 0;
  padding-left: 15pt;
}}
li {{
  font-size: 11pt;
  margin: 5pt 0;
  color: #2E4053;
}}
.img-box {{
  flex: 0 0 150pt;
  background: #FFFFFF;
  border-radius: 8pt;
  padding: 8pt;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.img-box img {{
  width: 100%;
  height: auto;
  border-radius: 6pt;
}}
</style>
</head>
<body>
<div class="container">
  <div class="content">
    <div class="header">
      <h1>{title}</h1>
    </div>
    <ul>
"""
        for item in content[:5]:
            html += f"      <li>{item}</li>\n"
        html += """    </ul>
  </div>
"""
        if image_path:
            html += f'  <div class="img-box">\n    <img src="../images/{rel_image}" alt="image">\n  </div>\n'
        html += """</div>
</body>
</html>"""

        filepath = self.slides_dir / f"slide_{num:02d}.html"
        filepath.write_text(html, encoding='utf-8')
        return str(filepath)


# CLI
def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--prompt', help='Image prompt')
    parser.add_argument('--output', help='Output filename')
    parser.add_argument('--batch', help='Batch topics (comma separated)')

    args = parser.parse_args()

    gen = ImageGenerator()

    if args.prompt:
        output = args.output or "generated.png"
        result = gen.generate_image(args.prompt, output)
        if result:
            print(f"\n[SUCCESS] {result}")

    elif args.batch:
        topics = [t.strip() for t in args.batch.split(',')]
        results = gen.generate_batch(topics)
        print(f"\n[RESULTS]")
        for topic, path in results.items():
            print(f"  {topic}: {path}")


if __name__ == "__main__":
    main()
