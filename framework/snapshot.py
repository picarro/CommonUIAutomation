"""
Snapshot testing functionality for Storybook
"""
import json
from pathlib import Path
from typing import Any, Dict, Optional
from playwright.sync_api import Page
import sys

from framework.config_loader import get_config
config = get_config()
from framework.base import StorybookBase


class SnapshotTester(StorybookBase):
    """Class for snapshot testing of component state and structure"""
    
    def __init__(self, page: Page, storybook_url: str = None):
        super().__init__(page, storybook_url)
        self.snapshots_dir = config.SNAPSHOTS_DIR
        
    def capture_snapshot(
        self,
        story_path: str,
        name: str,
        include_html: bool = False,
        include_styles: bool = False
    ) -> Dict[str, Any]:
        """
        Capture a snapshot of the component's current state
        
        Args:
            story_path: Path to the story
            name: Name for the snapshot
            include_html: Whether to include HTML structure
            include_styles: Whether to include computed styles
            
        Returns:
            Dictionary containing snapshot data
        """
        snapshot = {
            "story_path": story_path,
            "name": name,
            "state": self.get_component_state(),
            "timestamp": self.page.evaluate("() => Date.now()"),
        }
        
        if include_html:
            snapshot["html"] = self._capture_html()
        
        if include_styles:
            snapshot["styles"] = self._capture_styles()
        
        return snapshot
    
    def _capture_html(self, selector: str = ".sb-story") -> str:
        """Capture HTML structure of the component"""
        return self.page.locator(selector).inner_html()
    
    def _capture_styles(self, selector: str = ".sb-story") -> Dict[str, Any]:
        """Capture computed styles of the component"""
        return self.page.evaluate(f"""() => {{
            const element = document.querySelector('{selector}');
            if (!element) return {{}};
            const styles = window.getComputedStyle(element);
            return {{
                display: styles.display,
                visibility: styles.visibility,
                opacity: styles.opacity,
                width: styles.width,
                height: styles.height,
                backgroundColor: styles.backgroundColor,
                color: styles.color,
                fontSize: styles.fontSize,
                fontWeight: styles.fontWeight,
                margin: styles.margin,
                padding: styles.padding,
                border: styles.border,
            }};
        }}""")
    
    def save_snapshot(
        self,
        story_path: str,
        name: str,
        snapshot_data: Dict[str, Any],
        update: bool = False
    ) -> Path:
        """
        Save snapshot to file
        
        Args:
            story_path: Path to the story
            name: Name for the snapshot
            snapshot_data: Snapshot data dictionary
            update: Whether to update existing snapshot
            
        Returns:
            Path to the snapshot file
        """
        # Create directory structure: snapshots/{story_path}/
        story_dir = self.snapshots_dir / story_path.replace("--", "/")
        story_dir.mkdir(parents=True, exist_ok=True)
        
        snapshot_path = story_dir / f"{name}.json"
        
        if snapshot_path.exists() and not update:
            raise FileExistsError(
                f"Snapshot already exists: {snapshot_path}. "
                "Set update=True to overwrite."
            )
        
        with open(snapshot_path, "w") as f:
            json.dump(snapshot_data, f, indent=2)
        
        return snapshot_path
    
    def load_snapshot(self, story_path: str, name: str) -> Dict[str, Any]:
        """
        Load snapshot from file
        
        Args:
            story_path: Path to the story
            name: Name of the snapshot
            
        Returns:
            Snapshot data dictionary
        """
        story_dir = self.snapshots_dir / story_path.replace("--", "/")
        snapshot_path = story_dir / f"{name}.json"
        
        if not snapshot_path.exists():
            raise FileNotFoundError(f"Snapshot not found: {snapshot_path}")
        
        with open(snapshot_path, "r") as f:
            return json.load(f)
    
    def compare_snapshot(
        self,
        story_path: str,
        name: str,
        current_snapshot: Dict[str, Any],
        ignore_keys: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Compare current snapshot with saved baseline
        
        Args:
            story_path: Path to the story
            name: Name of the snapshot
            current_snapshot: Current snapshot data
            ignore_keys: Keys to ignore in comparison
            
        Returns:
            Dictionary with comparison results
        """
        ignore_keys = ignore_keys or ["timestamp"]
        
        try:
            baseline = self.load_snapshot(story_path, name)
        except FileNotFoundError:
            return {
                "match": False,
                "error": "Baseline snapshot not found",
                "baseline": None,
                "current": current_snapshot
            }
        
        # Filter out ignored keys
        baseline_filtered = {
            k: v for k, v in baseline.items() if k not in ignore_keys
        }
        current_filtered = {
            k: v for k, v in current_snapshot.items() if k not in ignore_keys
        }
        
        # Deep comparison
        differences = self._find_differences(baseline_filtered, current_filtered)
        
        return {
            "match": len(differences) == 0,
            "differences": differences,
            "baseline": baseline_filtered,
            "current": current_filtered
        }
    
    def _find_differences(
        self,
        baseline: Dict[str, Any],
        current: Dict[str, Any],
        path: str = ""
    ) -> list:
        """Recursively find differences between two dictionaries"""
        differences = []
        
        # Check for keys in baseline but not in current
        for key in baseline:
            current_path = f"{path}.{key}" if path else key
            if key not in current:
                differences.append({
                    "path": current_path,
                    "type": "missing",
                    "baseline": baseline[key],
                    "current": None
                })
            elif isinstance(baseline[key], dict) and isinstance(current[key], dict):
                differences.extend(
                    self._find_differences(baseline[key], current[key], current_path)
                )
            elif baseline[key] != current[key]:
                differences.append({
                    "path": current_path,
                    "type": "changed",
                    "baseline": baseline[key],
                    "current": current[key]
                })
        
        # Check for keys in current but not in baseline
        for key in current:
            if key not in baseline:
                current_path = f"{path}.{key}" if path else key
                differences.append({
                    "path": current_path,
                    "type": "added",
                    "baseline": None,
                    "current": current[key]
                })
        
        return differences
    
    def assert_snapshot(
        self,
        story_path: str,
        name: str,
        include_html: bool = False,
        include_styles: bool = False,
        ignore_keys: Optional[list] = None,
        update: bool = False
    ):
        """
        Assert that current snapshot matches baseline
        
        Args:
            story_path: Path to the story
            name: Name of the snapshot
            include_html: Whether to include HTML in snapshot
            include_styles: Whether to include styles in snapshot
            ignore_keys: Keys to ignore in comparison
            update: Whether to update baseline instead of comparing
        """
        # Capture current snapshot
        current = self.capture_snapshot(
            story_path, name, include_html=include_html, include_styles=include_styles
        )
        
        if update:
            # Update baseline
            self.save_snapshot(story_path, name, current, update=True)
            return
        
        # Compare with baseline
        comparison = self.compare_snapshot(story_path, name, current, ignore_keys)
        
        if not comparison["match"]:
            error_msg = f"Snapshot mismatch for {story_path}/{name}\n"
            error_msg += f"Differences: {json.dumps(comparison['differences'], indent=2)}"
            raise AssertionError(error_msg)

