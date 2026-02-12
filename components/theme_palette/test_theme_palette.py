"""
Theme Palette tests – verify Storybook theme palette CSS variables in all 4 modes.
Storybook: https://picarro.github.io/picarro-common-ui/?path=/story/theme-palette--theme-palette

Modes (Storybook globals.themeMode): light, light-hc, dark, dark-hc (URL &globals=themeMode:<mode>).
Each mode verifies against its own file: colors-light.properties, colors-light-hc.properties,
colors-dark.properties, colors-dark-hc.properties.
"""
import pytest
from pathlib import Path
from typing import Optional, Dict
from framework.base import PropertyChecker
from utils.logger import logger


STORY_PATH = "theme-palette--theme-palette"
THEME_MODES = ("light", "light-hc", "dark", "dark-hc")
_COMP_DIR = Path(__file__).parent


class _ThemePaletteTester(PropertyChecker):
    """Test-only helper: overrides load_css_variables to use a file path set by the test."""

    _css_properties_file: Optional[Path] = None

    def load_css_variables(self, component_name: Optional[str] = None) -> Dict[str, str]:
        if self._css_properties_file is not None:
            return self.load_css_variables_from_file(self._css_properties_file)
        return super().load_css_variables(component_name)


@pytest.mark.property
@pytest.mark.visual
class TestThemePalette:
    """Test suite for Theme Palette – CSS variables match .properties in each theme mode."""

    @pytest.fixture(scope="class")
    def component(self, page):
        return _ThemePaletteTester(page)

    @pytest.mark.parametrize("theme_mode", THEME_MODES, ids=THEME_MODES)
    def test_theme_palette_css_variables(self, component, theme_mode):
        """
        For the given theme mode, navigate with globals.themeMode=<mode>,
        then verify :root CSS variables against colors-<mode>.properties.
        """
        component._css_properties_file = _COMP_DIR / f"colors-{theme_mode}.properties"
        logger.info("Theme mode: %s → verifying against %s", theme_mode, component._css_properties_file.name)
        component.navigate_to_story(STORY_PATH, theme_mode=theme_mode, wait_for_selector="body")
        component.verify_all_css_variables(story_path=STORY_PATH, selector="body")
        logger.info("Theme palette variables verified for mode: %s", theme_mode)
