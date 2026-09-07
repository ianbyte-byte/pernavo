import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "frontend-wireframe" / "SKILL.md"
STYLE = ROOT / "skills" / "frontend-wireframe" / "references" / "style-system.md"
COLOR = ROOT / "skills" / "frontend-wireframe" / "references" / "color-system.md"
PALETTES = ROOT / "skills" / "frontend-wireframe" / "references" / "brand-palettes.md"
SHELL = ROOT / "skills" / "frontend-wireframe" / "assets" / "shell.html"


class FrontendWireframeContractTests(unittest.TestCase):
    def test_triggers_and_boundaries(self):
        contract = SKILL.read_text(encoding="utf-8")

        self.assertIn("线稿", contract)
        self.assertIn("wireframe", contract)
        self.assertIn("Do not use for production frontend", contract)
        self.assertIn("`engineering-workflow`", contract)
        self.assertIn("`report-writer`", contract)

    def test_single_file_html_deck(self):
        contract = SKILL.read_text(encoding="utf-8")

        self.assertIn("one HTML file", contract)
        self.assertIn("no CDN", contract)
        self.assertIn("file://", contract)
        self.assertIn("data-view=\"wireframe\"", contract)
        self.assertIn("[assets/shell.html](assets/shell.html)", contract)
        self.assertIn("[style system](references/style-system.md)", contract)
        self.assertIn("[color system](references/color-system.md)", contract)
        self.assertIn("Do not default to `#007AFF`", contract)

    def test_style_system_has_view_theme_mode(self):
        style = STYLE.read_text(encoding="utf-8")

        self.assertIn("data-view", style)
        self.assertIn("data-mode", style)
        self.assertIn("--bg-canvas", style)
        self.assertIn(".mac-window", style)
        self.assertIn(".browser-window", style)
        self.assertIn("No CDN", style)
        self.assertIn("color-system.md", style)
        self.assertIn('"Source Han Sans SC"', style)
        self.assertIn("overflow:hidden", style)
        self.assertIn("overflow:visible", style)

    def test_color_recipe_is_user_then_project_then_catalog(self):
        color = COLOR.read_text(encoding="utf-8")
        contract = SKILL.read_text(encoding="utf-8")

        self.assertIn("User.", color)
        self.assertIn("DESIGN.md", color)
        self.assertIn("Catalog fallback", color)
        self.assertIn("At most two chromatic plates", color)
        self.assertIn("#007AFF", color)
        self.assertIn("Color recipe (source · plates · hex):", contract)

    def test_named_palette_is_fixed_and_no_repaint(self):
        color = COLOR.read_text(encoding="utf-8")
        contract = SKILL.read_text(encoding="utf-8")

        self.assertIn("商务蓝", color)
        self.assertIn("never silently swap it for another hue", color)
        self.assertIn("never repaint the", color)
        self.assertIn("an accent never becomes a full-bleed background", contract)
        self.assertIn("4.5:1 (WCAG AA)", color)
        self.assertIn("3:1", color)
        self.assertIn("pure black `#000`", color)
        self.assertIn("Source Han Sans first", contract)

    def test_line_art_is_default_color_is_opt_in(self):
        contract = SKILL.read_text(encoding="utf-8")
        color = COLOR.read_text(encoding="utf-8")

        self.assertIn("Line-art principle", contract)
        self.assertIn("line art", contract)
        self.assertIn("when the client asks for them", contract)
        self.assertIn("If the brief is silent on color, ship line art", contract)
        self.assertIn("opt-in layer", color)
        self.assertIn("not the default skin", color)

    def test_brand_palettes_are_a_reference_not_identity(self):
        palettes = PALETTES.read_text(encoding="utf-8")
        contract = SKILL.read_text(encoding="utf-8")

        self.assertIn("Real Brands", palettes)
        self.assertIn("Atlassian", palettes)
        self.assertIn("Nubank", palettes)
        self.assertIn("Mercado Livre", palettes)
        self.assertIn("Do **not** clone a brand as this product's identity", palettes)
        self.assertIn("colors:", palettes)
        self.assertIn("primary", palettes)
        self.assertIn("brand palettes](references/brand-palettes.md)", contract)

    def test_shell_is_self_contained(self):
        shell = SHELL.read_text(encoding="utf-8")

        self.assertIn("<!doctype html>", shell)
        self.assertIn('data-view="wireframe"', shell)
        self.assertIn("data-view-btn", shell)
        self.assertIn("data-theme-btn", shell)
        self.assertIn("data-mode-btn", shell)
        self.assertNotIn("http://", shell)
        self.assertNotIn("https://", shell)
        self.assertNotIn("cdn.", shell)
