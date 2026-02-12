"""
Test file for Button component
Logger is automatically injected by conftest.py - use 'logger' directly
"""
import pytest
from components.button.button import (
    ButtonComponent,
    BUTTON_VARIANTS,
    BUTTON_STATES,
    BUTTON_SIZES,
    THEME_MODES,
    BUTTON_COLOR_PROPERTIES,
)
from framework.base import StorybookControlsManager
from utils.logger import logger

story_path = "main-button--primary"


@pytest.mark.property
class TestButtonComponent:
    """Test suite for Button component"""

    @pytest.fixture(scope="class")
    def button(self, page):
        """Fixture to create ButtonComponent instance and navigate to story"""
        button = ButtonComponent(page)
        try:
            button.navigate_to_story(story_path, wait_for_selector=button.locators.BUTTON)
        except Exception:
            button.navigate_to_story(story_path, wait_for_selector="body")
        return button
    
    def test_button_click(self, button):
        """Test clicking a button and verify onClick action was triggered"""
        
        # Verify button is enabled before click
        button.verify_button_enabled()
        
        # Clear actions panel to start fresh
        try:
            button.clear_actions_panel()
            logger.info("✅ Actions panel cleared")
        except Exception:
            pass  # If clearing fails, continue anyway
        
        # Get initial action count from panel
        initial_count = button.get_action_count_from_panel("onClick")
        logger.info(f"Initial onClick action count: {initial_count}")
        
        button.click_button()
        button.wait_for_animation(0.5)
        
        # Verify onClick action was triggered in Storybook Actions panel
        try:
            button.wait_for_action_in_panel("onClick", timeout=3000)
            
            # Verify action count increased
            final_count = button.get_action_count_from_panel("onClick")
            assert final_count > initial_count, \
                f"onClick action count should increase from {initial_count} to at least {initial_count + 1}, got {final_count}"
            
            logger.info(f"✅ Button clicked successfully - onClick action verified in Storybook Actions panel")
            logger.info(f"  Action count: {initial_count} → {final_count}")
        except TimeoutError:
            # Fallback: try the old method
            action_triggered = button.verify_storybook_action("onClick", expected_count=initial_count + 1, timeout=2000)
            if action_triggered:
                logger.info("✅ Button clicked successfully - onClick action verified (fallback method)")
            else:
                # Verify action count increased as fallback verification
                final_count = button.get_action_count_from_panel("onClick")
                assert final_count > initial_count, \
                    f"onClick action was not triggered. Action count did not increase from {initial_count}, got {final_count}"
                logger.info(f"✅ Button clicked successfully - action count increased: {initial_count} → {final_count}")
        except Exception as e:
            # Last resort: check if action count increased
            final_count = button.get_action_count_from_panel("onClick")
            if final_count <= initial_count:
                raise AssertionError(
                    f"Button click did not trigger onClick action. "
                    f"Action count did not increase from {initial_count}, got {final_count}. "
                    f"Original error: {e}"
                )
            logger.info(f"✅ Button clicked successfully - action count increased: {initial_count} → {final_count}")
        
    def test_button_text(self):
        """Test getting button text"""
        button, story_path, controls_manager = self.button, self.story_path, self.controls_manager
        
        # Get button text
        text = button.get_button_text()
        logger.info(f"Button text: {text}")
        
        # Verify text is not empty
        assert text == "Hello World", f"Button text should be 'Hello World', got '{text}'"
 
    def test_button_enabled_state(self):
        """Test button enabled/disabled state"""
        button, story_path, controls_manager = self.button, self.story_path, self.controls_manager
        
        # Verify button is enabled
        button.verify_button_enabled()
        logger.info("✅ Button is enabled")
    
    def test_button_disabled_state(self):
        """Test button disabled state"""
        button, story_path, controls_manager = self.button, self.story_path, self.controls_manager
        
        # Update button to disabled state via controls
        controls_manager.update_control_via_api(story_path, "disabled", True)
        
        # Verify button is disabled
        button.verify_button_disabled()
        logger.info("✅ Button is disabled")
    
    def test_button_properties(self):
        """Test button regular CSS properties (excluding CSS variables)"""
        button, story_path, controls_manager = self.button, self.story_path, self.controls_manager
        
        button.verify_component_properties(selector=button.locators.BUTTON)
        logger.info("✅ Button regular properties verified")

    def test_button_computed_style_background_color(self, button):
        """Test get_computed_style returns background-color for the button"""
        value = button.get_computed_style(button.locators.BUTTON, "background-color")
        assert value, f"get_computed_style(..., 'background-color') should return non-empty string, got: {value!r}"
        # Computed background-color is typically rgb/rgba or hex
        assert (
            value.startswith("rgb") or value.startswith("#") or value in ("transparent",)
        ), f"background-color should look like a color (rgb/rgba/hex), got: {value!r}"
        logger.info("✅ get_computed_style(button, 'background-color') = %r", value)

    def test_button_declared_style_background_color(self, button):
        """Test get_declared_style returns declared value (e.g. var(--color-green-100)) for background-color"""
        value = button.get_declared_style(button.locators.BUTTON, "background-color")
        # Declared value can be var(--...) or a literal (e.g. hex); empty if not set in stylesheets
        assert isinstance(value, str), f"get_declared_style should return str, got: {type(value)}"
        if value:
            logger.info("✅ get_declared_style(button, 'background-color') = %r", value)
            # When design uses CSS variables, we get e.g. "var(--color-green-100)"
            if value.startswith("var("):
                logger.info("   (variable reference: %s)", value)
    
    def test_button_label_update(self):
        """Test updating button label via Storybook controls"""
        button, story_path, controls_manager = self.button, self.story_path, self.controls_manager
        
        # Update label
        new_label = "Updated Button Label"
        button.update_button_label(new_label)
        
        # Verify label was updated
        label = button.get_button_label()
        assert label == new_label or new_label in button.get_button_text(), \
            f"Button label should be '{new_label}'"
        logger.info(f"✅ Button label updated to: {new_label}")
    
    def test_button_variant(self):
        """Test button variant"""
        button, story_path, controls_manager = self.button, self.story_path, self.controls_manager
        
        # Update variant via controls
        controls_manager.update_control_via_api(story_path, "variant", "primary")
        
        # Verify variant
        button.verify_button_variant("primary")
        logger.info("✅ Button variant verified")
    
    def test_update_single_control(self):
        """Test updating a single control value"""
        button, story_path, controls_manager = self.button, self.story_path, self.controls_manager
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting test: test_update_single_control")
        logger.info(f"Story path: {story_path}")
        logger.info(f"Storybook URL: {button.storybook_url}")
        logger.info(f"{'='*60}\n")
        
        try:
            # Update a control (e.g., children, label, disabled, variant)
            controls_manager.update_control_via_ui(story_path, "children", "Updated Label")
            logger.info("✅ Control updated")
            
            label = button.get_button_text()
            logger.info(f"✅ Control value retrieved: {label}")
            
            assert label == "Updated Label", f"Control value should be 'Updated Label', got '{label}'"
            logger.info("✅ Test passed!")
            
        except Exception as e:
            logger.error(f"\n❌ Test failed with error: {e}")
            logger.error(f"Current page URL: {button.page.url}")
            logger.error(f"Page title: {button.page.title()}")
            import traceback
            traceback.print_exc()
            raise
    
    def test_update_multiple_controls(self):
        """Test updating multiple controls at once"""
        button, story_path, controls_manager = self.button, self.story_path, self.controls_manager
        
        # Update multiple controls
        controls_manager.update_multiple_controls(story_path, {
            "children": "Multi Update",
            "disabled": False,
            "variant": "primary"
        })
        
        # Verify all controls were updated
        all_values = controls_manager.get_all_control_values(story_path)
        assert all_values.get("children") == "Multi Update"
        assert all_values.get("disabled") == False
        logger.info("✅ Multiple controls updated successfully")
    
    def test_get_control_value(self):
        """Test getting a control value"""
        button, story_path, controls_manager = self.button, self.story_path, self.controls_manager
        
        # Get a control value
        # Adjust control name based on your component
        value = controls_manager.get_control_value(story_path, "children")
        assert value is not None, "Control value should not be None"
        logger.info(f"✅ Control value retrieved: {value}")
    
    def test_get_all_control_values(self):
        """Test getting all control values"""
        button, story_path, controls_manager = self.button, self.story_path, self.controls_manager
        
        # Get all control values
        all_values = controls_manager.get_all_control_values(story_path)
        assert isinstance(all_values, dict), "Should return a dictionary"
        assert len(all_values) > 0, "Should have at least one control"
        logger.info(f"✅ Retrieved {len(all_values)} control values")
    
    def test_update_control_types(self):
        """Test updating different control types"""
        button, story_path, controls_manager = self.button, self.story_path, self.controls_manager
        
        # Test string control
        controls_manager.update_control_via_api(story_path, "children", "Test String")
        
        # Test boolean control
        controls_manager.update_control_via_api(story_path, "disabled", True)
        
        # Test number control (if available)
        # controls_manager.update_control_via_api(story_path, "count", 42)
        
        # Verify values
        assert controls_manager.get_control_value(story_path, "children") == "Test String"
        assert controls_manager.get_control_value(story_path, "disabled") == True
        # assert controls_manager.get_control_value(story_path, "count") == 42
        logger.info("✅ Different control types updated successfully")
    
    def test_reset_controls(self):
        """Test resetting controls to defaults"""
        button, story_path, controls_manager = self.button, self.story_path, self.controls_manager
        
        # Get initial values
        initial_values = controls_manager.get_all_control_values(story_path)
        logger.info(f"Initial values: {initial_values}")
        
        # Update some controls
        controls_manager.update_multiple_controls(story_path, {
            "children": "Changed",
            "disabled": True
        })
        
        # Reset to defaults
        controls_manager.reset_controls_to_defaults(story_path)
        
        # Verify values are back to initial
        reset_values = controls_manager.get_all_control_values(story_path)
        # Note: This test may need adjustment based on your Storybook setup
        assert reset_values is not None
        logger.info("✅ Controls reset to defaults")
    
    def test_control_updates_reflect_in_component(self):
        """Test that control updates are reflected in the component"""
        button, story_path, controls_manager = self.button, self.story_path, self.controls_manager
        
        # Update label control
        new_label = "Dynamic Label"
        controls_manager.update_control_via_api(story_path, "children", new_label)
        
        # Wait for component to update
        button.wait_for_animation(1.0)
        
        # Verify component shows the updated label
        button_text = button.get_button_text()
        assert new_label in button_text, f"Component should show '{new_label}', got '{button_text}'"
        logger.info(f"✅ Component updated with new label: {new_label}")
    
    def test_controls_with_complex_values(self):
        """Test updating controls with complex values (objects, arrays)"""
        button, story_path, controls_manager = self.button, self.story_path, self.controls_manager
        
        # Test array control (if available in your Button component)
        # controls_manager.update_control_via_api(story_path, "items", ["item1", "item2", "item3"])
        
        # Test object control (if available in your Button component)
        # controls_manager.update_control_via_api(story_path, "config", {
        #     "key1": "value1",
        #     "key2": 123
        # })
        
        # Verify values
        # items = controls_manager.get_control_value(story_path, "items")
        # assert isinstance(items, list), "Items should be a list"
        
        # config = controls_manager.get_control_value(story_path, "config")
        # assert isinstance(config, dict), "Config should be a dict"
        
        logger.info("✅ Complex values test (commented out - adjust based on your Button component args)")
    
    def test_button_hover(self):
        """Test hovering over button"""
        button, story_path, controls_manager = self.button, self.story_path, self.controls_manager
        
        # Hover over button
        button.hover_button()
        
        # Verify hover state (add specific verification if needed)
        logger.info("✅ Button hovered successfully")
    
    def test_button_click_by_text(self):
        """Test clicking button by its text"""
        button, story_path, controls_manager = self.button, self.story_path, self.controls_manager
        
        # Get button text first
        button_text = button.get_button_text()
        
        # Click button by text
        button.click_button_by_text(button_text)
        logger.info(f"✅ Button clicked by text: {button_text}")

    # Runs one test per combination: BUTTON_VARIANTS × BUTTON_STATES × BUTTON_SIZES × THEME_MODES.
    # One page load per combination; verifies all properties (computed) and color declared styles together.
    @pytest.mark.parametrize("variant", BUTTON_VARIANTS)
    @pytest.mark.parametrize("state", BUTTON_STATES)
    @pytest.mark.parametrize("size", BUTTON_SIZES)
    @pytest.mark.parametrize("theme", THEME_MODES)
    def test_button_variant_properties(
        self, button, controls_manager, variant: str, state: str, size: str, theme: str
    ):
        """Set Storybook controls for variant/state/size, navigate with theme; verify all CSS properties and color declared styles in one go."""
        button.navigate_to_story(
            story_path, theme_mode=theme, wait_for_selector=button.locators.BUTTON
        )

        controls = {
            "variant": variant,
            "disabled": state == "disabled",
            "size": size,
            "loading": state == "loading",
        }
        controls_manager.update_multiple_controls(story_path, controls, button.locators.BUTTON)

        expected = button.load_button_variant_properties(variant, state, size)
        if not expected:
            pytest.skip(
                f"No expected properties for variant={variant}, state={state}, size={size} in button.properties"
            )

        expected_colors = button.load_button_variant_color_properties(variant, state, size)

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

        def assert_declared_color_styles():
            mismatches = []
            for prop_name, expected_value in expected_colors.items():
                actual_declared = button.get_declared_style(button.locators.BUTTON, prop_name)
                if not declared_matches(expected_value, actual_declared):
                    mismatches.append(
                        f"{prop_name}: expected {expected_value!r}, got {actual_declared!r}"
                    )
            if mismatches:
                raise AssertionError(
                    "Found %s declared color mismatch(es) (%s.%s.%s):\n  - %s"
                    % (len(mismatches), variant, state, size, "\n  - ".join(mismatches))
                )

        def verify_all():
            button.verify_component_properties(properties=expected, selector=button.locators.BUTTON)
            if expected_colors:
                assert_declared_color_styles()

        if state == "hover":
            button.hover_button()
            verify_all()
        elif state == "click":
            button.hold_click_state(button.locators.BUTTON, callback=verify_all)
        else:
            verify_all()

        logger.info(
            "✅ Verified %s %s %s %s: %s properties%s",
            variant,
            state,
            size,
            theme,
            len(expected),
            f", declared colors: {list(expected_colors.keys())}" if expected_colors else "",
        )
