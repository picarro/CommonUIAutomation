# Component Structure Guide

This framework uses a Page Object Model (POM) structure organized by component.

## Directory Structure

```
components/
├── __init__.py
├── base_component.py          # Base class with common functionality
├── button/
│   ├── __init__.py
│   ├── locators.py            # All Button locators/selectors
│   ├── button.py              # Button component functions
│   └── test_button.py        # Button test cases
├── checkbox/
│   ├── __init__.py
│   ├── locators.py            # All Checkbox locators/selectors
│   ├── checkbox.py            # Checkbox component functions
│   └── test_checkbox.py       # Checkbox test cases
└── [other-components]/
    ├── __init__.py
    ├── locators.py
    ├── [component].py
    └── test_[component].py
```

## File Responsibilities

### 1. `locators.py`
- Contains all CSS selectors and locators for the component
- Uses a class (e.g., `ButtonLocators`) to organize selectors
- Can have static methods for dynamic selectors
- Example:
  ```python
  class ButtonLocators:
      BUTTON = "button"
      BUTTON_PRIMARY = "button.btn-primary"
      
      @staticmethod
      def button_with_text(text: str) -> str:
          return f"button:has-text('{text}')"
  ```

### 2. `[component].py`
- Contains all component-specific functions
- Inherits from `BaseComponent`
- Uses locators from `locators.py`
- Implements component-specific actions and verifications
- Example:
  ```python
  class ButtonComponent(BaseComponent):
      def __init__(self, page: Page):
          super().__init__(page)
          self.locators = ButtonLocators()
      
      def click_button(self):
          self.page.locator(self.locators.BUTTON).click()
  ```

### 3. `test_[component].py`
- Contains all test cases for the component
- Uses the component class from `[component].py`
- Uses pytest fixtures (page, etc.)
- Example:
  ```python
  def test_button_click(page):
      button = ButtonComponent(page)
      button.navigate_to_story("main-button--button-story")
      button.click_button()
  ```

### 4. `base_component.py`
- Contains common functionality used by all components
- Inherits from `StorybookBase` and `PropertyChecker`
- Provides generic methods like:
  - `wait_for_component_ready()`
  - `is_component_visible()`
  - `get_component_attribute()`
  - `click_component()`
  - etc.

## Creating a New Component

1. **Create component folder:**
   ```bash
   mkdir -p components/mycomponent
   touch components/mycomponent/__init__.py
   ```

2. **Create `locators.py`:**
   ```python
   class MyComponentLocators:
       COMPONENT = "div.my-component"
       # Add more locators...
   ```

3. **Create `mycomponent.py`:**
   ```python
   from components.base_component import BaseComponent
   from components.mycomponent.locators import MyComponentLocators
   
   class MyComponent(BaseComponent):
       def __init__(self, page: Page):
           super().__init__(page)
           self.locators = MyComponentLocators()
       
       # Add component-specific methods...
   ```

4. **Create `test_mycomponent.py`:**
   ```python
   import pytest
   from components.mycomponent.mycomponent import MyComponent
   
   def test_mycomponent_action(page):
       component = MyComponent(page)
       component.navigate_to_story("main-mycomponent--story")
       # Add test logic...
   ```

## Benefits

- **Separation of Concerns**: Locators, functions, and tests are separated
- **Reusability**: Component functions can be reused across tests
- **Maintainability**: Easy to update locators or functions in one place
- **Scalability**: Easy to add new components following the same pattern
- **Organization**: Clear structure makes it easy to find component code

## Running Tests

Run all component tests:
```bash
pytest components/ -v
```

Run tests for a specific component:
```bash
pytest components/button/test_button.py -v
```

Run a specific test:
```bash
pytest components/button/test_button.py::TestButtonComponent::test_button_click -v
```

