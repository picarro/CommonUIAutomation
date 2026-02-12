"""
Snapshot tests for Storybook components
"""
import pytest
from framework.snapshot import SnapshotTester


@pytest.mark.snapshot
class TestSnapshots:
    """Snapshot test suite"""
    
    def test_component_snapshot(self, snapshot_tester: SnapshotTester):
        """Test component snapshot capture and comparison"""
        story_path = "example-button--primary"
        snapshot_tester.navigate_to_story(story_path)
        
        # Assert snapshot matches baseline
        # First run will create baseline, subsequent runs will compare
        snapshot_tester.assert_snapshot(
            story_path=story_path,
            name="default",
            include_html=False,
            include_styles=False
        )
    
    def test_component_snapshot_with_html(self, snapshot_tester: SnapshotTester):
        """Test component snapshot with HTML structure"""
        story_path = "example-button--primary"
        snapshot_tester.navigate_to_story(story_path)
        
        snapshot_tester.assert_snapshot(
            story_path=story_path,
            name="with_html",
            include_html=True,
            include_styles=False
        )
    
    def test_component_snapshot_with_styles(self, snapshot_tester: SnapshotTester):
        """Test component snapshot with computed styles"""
        story_path = "example-button--primary"
        snapshot_tester.navigate_to_story(story_path)
        
        snapshot_tester.assert_snapshot(
            story_path=story_path,
            name="with_styles",
            include_html=False,
            include_styles=True
        )
    
    def test_component_snapshot_full(self, snapshot_tester: SnapshotTester):
        """Test component snapshot with HTML and styles"""
        story_path = "example-button--primary"
        snapshot_tester.navigate_to_story(story_path)
        
        snapshot_tester.assert_snapshot(
            story_path=story_path,
            name="full",
            include_html=True,
            include_styles=True
        )
    
    def test_component_snapshot_after_interaction(self, snapshot_tester: SnapshotTester):
        """Test component snapshot after user interaction"""
        story_path = "example-button--primary"
        snapshot_tester.navigate_to_story(story_path)
        
        # Perform interaction
        snapshot_tester.click("button")
        
        # Capture snapshot after interaction
        snapshot_tester.assert_snapshot(
            story_path=story_path,
            name="after_click",
            include_html=False,
            include_styles=False
        )
    
    def test_component_snapshot_multiple_states(self, snapshot_tester: SnapshotTester):
        """Test component snapshots for multiple states"""
        story_path = "example-button--primary"
        snapshot_tester.navigate_to_story(story_path)
        
        # Default state
        snapshot_tester.assert_snapshot(
            story_path=story_path,
            name="state_default",
            include_html=False,
            include_styles=False
        )
        
        # Hover state
        snapshot_tester.hover("button")
        snapshot_tester.assert_snapshot(
            story_path=story_path,
            name="state_hover",
            include_html=False,
            include_styles=False
        )
        
        # Clicked state
        snapshot_tester.click("button")
        snapshot_tester.assert_snapshot(
            story_path=story_path,
            name="state_clicked",
            include_html=False,
            include_styles=False
        )

