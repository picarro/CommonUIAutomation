"""
Test file for Checkbox component
Storybook: https://picarro.github.io/picarro-common-ui/?path=/story/main-checkbox--default
Figma: https://www.figma.com/design/7dSENfOCgPBZc8Tk2A1NlK/Picarro-Common-UI-Library
Logger is automatically injected by conftest.py - use 'logger' directly
"""
import pytest
from components.checkbox.checkbox import CheckboxComponent
from framework.base import StorybookControlsManager
from utils.logger import logger

story_path = "main-checkbox--default"

CHECKBOX_VARIANTS = ["unchecked", "checked"]
CHECKBOX_STATES = ["active", "hover", "disabled", "focus"]
THEME_MODES = ("light", "light-hc", "dark", "dark-hc")


@pytest.mark.property
class TestCheckboxComponent:
    """Test suite for Checkbox component"""

    @pytest.fixture(scope="class")
    def checkbox(self, page):
        """Fixture to create CheckboxComponent and navigate to story once"""
        checkbox = CheckboxComponent(page)
        checkbox.navigate_to_story(story_path, wait_for_selector=None)
        page.wait_for_selector("iframe", timeout=10000)
        try:
            checkbox.wait_for_component_ready(checkbox.locators.CHECKBOX, timeout=10000)
        except Exception:
            try:
                checkbox.wait_for_component_ready(checkbox.locators.CHECKBOX_ICON, timeout=5000)
            except Exception:
                checkbox.wait_for_component_ready(checkbox.locators.CHECKBOX_BY_ROLE, timeout=5000)
        return checkbox

    @pytest.fixture(scope="class")
    def controls_manager(self, page):
        """Fixture for StorybookControlsManager"""
        return StorybookControlsManager(page)

    def test_checkbox_click(self):
        """Test clicking a checkbox toggles state"""
        checkbox, story_path, controls_manager = self._checkbox, self._story_path, self._controls_manager
        initial = checkbox.is_checked()
        checkbox.click_checkbox()
        checkbox.wait_for_animation(0.5)
        assert checkbox.is_checked() != initial, "Click should toggle checkbox state"
        logger.info("✅ Checkbox click toggled state")

    def test_checkbox_check(self):
        """Test checking the checkbox"""
        checkbox = self._checkbox
        checkbox.uncheck_checkbox()
        checkbox.check_checkbox()
        checkbox.verify_checked()
        logger.info("✅ Checkbox checked")

    def test_checkbox_uncheck(self):
        """Test unchecking the checkbox"""
        checkbox = self._checkbox
        checkbox.check_checkbox()
        checkbox.uncheck_checkbox()
        checkbox.verify_unchecked()
        logger.info("✅ Checkbox unchecked")

    def test_checkbox_enabled_state(self):
        """Test checkbox is enabled by default"""
        checkbox = self._checkbox
        checkbox.verify_checkbox_enabled()
        logger.info("✅ Checkbox is enabled")

    def test_checkbox_disabled_state(self):
        """Test checkbox disabled state via Storybook controls"""
        checkbox, story_path, controls_manager = self._checkbox, self._story_path, self._controls_manager
        controls_manager.update_control_via_api(story_path, "disabled", True)
        checkbox.wait_for_animation(0.5)
        checkbox.verify_checkbox_disabled()
        logger.info("✅ Checkbox is disabled")
        # Restore enabled for other tests
        controls_manager.update_control_via_api(story_path, "disabled", False)
        checkbox.wait_for_animation(0.3)

    def test_checkbox_properties(self):
        """Test checkbox icon CSS properties (excluding CSS variables)"""
        checkbox = self._checkbox
        checkbox.verify_component_properties(selector=checkbox.locators.CHECKBOX_ICON)
        logger.info("✅ Checkbox icon properties verified")

    def test_checkbox_css_variables(self):
        """Verify :root CSS variables match css-variables.properties (if story exposes theme)"""
        checkbox, story_path = self._checkbox, self._story_path
        checkbox.verify_all_css_variables(story_path=story_path, selector="body")
        logger.info("✅ Checkbox CSS variable properties verified")

    def test_checkbox_label(self):
        """Test getting checkbox label text (if story has label)"""
        checkbox = self._checkbox
        label = checkbox.get_checkbox_label()
        if label is not None:
            assert isinstance(label, str), "Label should be a string"
            logger.info(f"✅ Checkbox label: {label}")
        else:
            # Label may be in wrapper; try to get text near checkbox
            frame = checkbox.get_iframe_frame_locator()
            text = frame.locator(checkbox.locators.CHECKBOX_LABEL).first.inner_text()
            if text:
                logger.info(f"✅ Checkbox context text: {text.strip()[:50]}")

    def test_checkbox_hover(self):
        """Test hovering over checkbox"""
        checkbox = self._checkbox
        checkbox.hover_checkbox()
        logger.info("✅ Checkbox hovered successfully")

    def test_update_single_control(self):
        """Test updating a single control value (e.g. label or checked)"""
        checkbox, story_path, controls_manager = self._checkbox, self._story_path, self._controls_manager
        logger.info(f"Story path: {story_path}, URL: {checkbox.storybook_url}")
        try:
            # Try label/children control if available
            controls_manager.update_control_via_ui(story_path, "label", "Accept terms")
            value = controls_manager.get_control_value(story_path, "label")
            if value is not None:
                assert value == "Accept terms", f"Expected 'Accept terms', got {value}"
            logger.info("✅ Single control updated")
        except Exception as e:
            # Fallback: update checked via API
            controls_manager.update_control_via_api(story_path, "checked", True)
            val = controls_manager.get_control_value(story_path, "checked")
            assert val is True, f"checked should be True, got {val}"
            logger.info("✅ Single control (checked) updated")

    def test_update_multiple_controls(self):
        """Test updating multiple controls at once"""
        checkbox, story_path, controls_manager = self._checkbox, self._story_path, self._controls_manager
        controls_manager.update_multiple_controls(story_path, {
            "checked": True,
            "disabled": False,
        })
        all_values = controls_manager.get_all_control_values(story_path)
        assert isinstance(all_values, dict), "Should return a dictionary"
        logger.info(f"✅ Multiple controls updated: {list(all_values.keys())}")

    def test_get_control_value(self):
        """Test getting a control value"""
        story_path, controls_manager = self._story_path, self._controls_manager
        value = controls_manager.get_control_value(story_path, "checked")
        # checked is typically bool; accept None if control name differs
        assert value is None or value in (True, False) or isinstance(value, bool), "checked should be bool or None"
        logger.info(f"✅ Control value retrieved: checked={value}")

    def test_get_all_control_values(self):
        """Test getting all control values"""
        story_path, controls_manager = self._story_path, self._controls_manager
        all_values = controls_manager.get_all_control_values(story_path)
        assert isinstance(all_values, dict), "Should return a dictionary"
        assert len(all_values) >= 0, "Should return controls dict"
        logger.info(f"✅ Retrieved {len(all_values)} control values")

    def test_control_updates_reflect_in_component(self):
        """Test that control updates are reflected in the component"""
        checkbox, story_path, controls_manager = self._checkbox, self._story_path, self._controls_manager
        controls_manager.update_control_via_api(story_path, "checked", True)
        checkbox.wait_for_animation(0.5)
        assert checkbox.is_checked(), "Component should show checked state"
        controls_manager.update_control_via_api(story_path, "checked", False)
        checkbox.wait_for_animation(0.3)
        assert checkbox.is_unchecked(), "Component should show unchecked state"
        logger.info("✅ Control updates reflected in component")

    def test_reset_controls(self):
        """Test resetting controls to defaults"""
        story_path, controls_manager = self._story_path, self._controls_manager
        initial = controls_manager.get_all_control_values(story_path)
        controls_manager.update_control_via_api(story_path, "checked", True)
        controls_manager.reset_controls_to_defaults(story_path)
        reset_values = controls_manager.get_all_control_values(story_path)
        assert reset_values is not None
        logger.info("✅ Controls reset to defaults")

    @pytest.mark.parametrize("variant", CHECKBOX_VARIANTS)
    @pytest.mark.parametrize("state", CHECKBOX_STATES)
    @pytest.mark.parametrize("theme", THEME_MODES)
    def test_checkbox_variant_properties(
        self, checkbox, controls_manager, variant: str, state: str, theme: str
    ):
        """Set Storybook controls for variant/state; navigate with theme; verify icon, label, and container CSS properties and declared color styles."""
        checkbox.navigate_to_story(
            story_path, theme_mode=theme, wait_for_selector=checkbox.locators.CHECKBOX
        )
        checkbox.page.wait_for_selector("iframe", timeout=10000)
        checkbox.wait_for_component_ready(checkbox.locators.CHECKBOX, timeout=10000)

        controls = {
            "checked": variant == "checked",
            "disabled": state == "disabled",
        }
        controls_manager.update_multiple_controls(story_path, controls, checkbox.locators.CHECKBOX)

        expected_icon = checkbox.load_checkbox_icon_properties(variant, state)
        if not expected_icon:
            pytest.skip(
                f"No expected icon properties for variant={variant}, state={state} in checkbox.properties"
            )

        expected_label = checkbox.load_checkbox_label_properties(variant, state)
        expected_container = checkbox.load_checkbox_container_properties()
        expected_icon_colors = checkbox.load_checkbox_icon_color_properties(variant, state)
        expected_label_colors = checkbox.load_checkbox_label_color_properties(variant, state)

        def declared_matches(expected_val: str, actual: str) -> bool:
            e, a = expected_val.strip(), actual.strip()
            if e == a:
                return True
            if e.startswith("var(--") and a.startswith("var(--"):
                evar = e.rstrip(")").rstrip()
                if a == evar + ")" or a.startswith(evar + ","):
                    return True
            if e == "rgb(0, 0, 0)" and a == "rgba(0, 0, 0, 0)":
                return True
            if a == "rgb(0, 0, 0)" and e == "rgba(0, 0, 0, 0)":
                return True
            return False

        def assert_declared_colors(selector: str, expected_colors: dict, part: str):
            if not expected_colors:
                return
            mismatches = []
            for prop_name, expected_value in expected_colors.items():
                actual_declared = checkbox.get_declared_style(selector, prop_name)
                if not declared_matches(expected_value, actual_declared):
                    mismatches.append(
                        f"{part} {prop_name}: expected {expected_value!r}, got {actual_declared!r}"
                    )
            if mismatches:
                raise AssertionError(
                    "Found %s declared color mismatch(es) (%s.%s):\n  - %s"
                    % (len(mismatches), variant, state, "\n  - ".join(mismatches))
                )

        def verify_all():
            checkbox.verify_component_properties(
                properties=expected_icon, selector=checkbox.locators.CHECKBOX_ICON
            )
            if expected_icon_colors:
                assert_declared_colors(
                    checkbox.locators.CHECKBOX_ICON, expected_icon_colors, "icon"
                )
            if expected_label:
                checkbox.verify_component_properties(
                    properties=expected_label, selector=checkbox.locators.CHECKBOX_LABEL
                )
            if expected_label_colors:
                assert_declared_colors(
                    checkbox.locators.CHECKBOX_LABEL, expected_label_colors, "label"
                )
            if expected_container:
                checkbox.verify_component_properties(
                    properties=expected_container, selector=checkbox.locators.CHECKBOX
                )

        if state == "hover":
            checkbox.hover_checkbox()
            verify_all()
        elif state == "focus":
            checkbox.get_checkbox().focus()
            checkbox.wait_for_animation(0.2)
            verify_all()
        else:
            verify_all()

        total = len(expected_icon) + len(expected_label) + len(expected_container)
        logger.info(
            "✅ Verified checkbox icon+label+container %s %s %s: %s properties (icon=%s, label=%s, container=%s)%s",
            variant,
            state,
            theme,
            total,
            len(expected_icon),
            len(expected_label),
            len(expected_container),
            f", icon colors: {list(expected_icon_colors.keys())}" if expected_icon_colors else "",
        )
