import logging

"""
Lightweight logger helper.

Handlers/formatters are configured once in root `conftest.py`. This helper only
returns a named logger; it does not add handlers (prevents duplicates).
"""

def get_logger(name: str = "commonui") -> logging.Logger:
    """
    Return a project logger (or named child) without adding handlers.

    Args:
      - name (str): Logger name to use. Common patterns:
          - 'commonui'                       (project root logger)
          - 'commonui.components.Button'     (component/class logger)
          - 'commonui.tests'                 (tests logger)
          - 'commonui.framework.something'   (framework code)

    Returns:
      - logging.Logger: Logger instance (handlers configured elsewhere).
    """
    return logging.getLogger(name)


# Default logger instance - can be imported directly
logger = get_logger()

