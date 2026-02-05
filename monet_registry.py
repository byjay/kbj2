import json
import os
from datetime import datetime

class MonetRegistry:
    """
    KBJ2 Implementation of Monet Registry (Component Store).
    'Ported' from GitHub to Local Enterprise Storage.
    """
    def __init__(self, registry_path=r"F:\kbj2\MONET_REGISTRY.json"):
        self.registry_path = registry_path
        self.components = {}
        self.load_registry()

    def load_registry(self):
        if os.path.exists(self.registry_path):
            with open(self.registry_path, "r", encoding="utf-8") as f:
                self.components = json.load(f)
        else:
            # Seed with 'Ported' Data (Simulating Download)
            self.components = {
                "auth_login_001": {
                    "type": "Authentication",
                    "name": "Glassmorphism Login",
                    "code": "<div class='glass-login'>...</div>",
                    "tags": ["modern", "glass", "dark_mode"]
                },
                "hero_section_002": {
                    "type": "Landing",
                    "name": "SaaS Hero Gradient",
                    "code": "<section class='hero-gradient'>...</section>",
                    "tags": ["saas", "hero", "gradient"]
                },
                "navbar_responsive_005": {
                    "type": "Navigation",
                    "name": "Responsive Mobile Nav",
                    "code": "<nav class='mobile-nav'>...</nav>",
                    "tags": ["mobile", "responsive"]
                }
            }
            self.save_registry()

    def save_registry(self):
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(self.components, f, ensure_ascii=False, indent=2)

    def register_component(self, comp_id, data):
        """Scraper Agents call this"""
        self.components[comp_id] = data
        self.save_registry()
        return f"Component {comp_id} Registered."

    def get_component(self, criteria):
        """Builder Agents call this"""
        # Simple match for simulation
        for cid, data in self.components.items():
            if criteria.lower() in data['name'].lower() or criteria.lower() in data['type'].lower():
                return data
        return None

# Singleton Instance
monet_registry = MonetRegistry()
