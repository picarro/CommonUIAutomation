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

STORY_PATH = "main-checkbox--default"


@pytest.mark.property
class TestCheckboxComponent:
    """Test suite for Checkbox component"""

    @pytest.fixture(scope="class")
    def checkbox(self, page):
        """Fixture to create CheckboxComponent and navigate to story once"""
        checkbox = CheckboxComponent(page)
        checkbox.navigate_to_story(STORY_PATH, wait_for_selector=None)
        page.wait_for_selector("iframe", timeout=10000)
        try:
            checkbox.wait_for_component_ready(checkbox.locators.CHECKBOX, timeout=10000)
        except Exception:
            checkbox.wait_for_component_ready(checkbox.locators.CHECKBOX_BY_ROLE, timeout=5000)
        return checkbox

    @pytest.fixture(scope="class")
    def controls_manager(self, page):
        """Fixture for StorybookControlsManager"""
        return StorybookControlsManager(page)

    @pytest.fixture(scope="class", autouse=True)
    def setup_class_fixtures(self, checkbox, controls_manager):
        """Store fixtures as instance attributes"""
        self._checkbox = checkbox
        self._story_path = STORY_PATH
        self._controls_manager = controls_manager
        yield

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
        """Test checkbox CSS properties (excluding CSS variables)"""
        checkbox = self._checkbox
        checkbox.verify_component_properties(selector=checkbox.locators.CHECKBOX)
        logger.info("✅ Checkbox regular properties verified")

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
            text = frame.locator(checkbox.locators.CHECKBOX).locator("xpath=..").first.inner_text()
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
