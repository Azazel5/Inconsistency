import math
import unittest
from backend.analyzer import calculate_linear_regression, fit_curves, analyze_playlist_data

class TestAnalysisMath(unittest.TestCase):
    
    def test_linear_regression(self):
        # Test basic linear regression: y = 2x + 1
        x = [1.0, 2.0, 3.0, 4.0]
        y = [3.0, 5.0, 7.0, 9.0]
        slope, intercept, r2 = calculate_linear_regression(x, y)
        
        self.assertAlmostEqual(slope, 2.0)
        self.assertAlmostEqual(intercept, 1.0)
        self.assertAlmostEqual(r2, 1.0)
        
        # Test constant values (avoid divide by zero)
        x_const = [1.0, 1.0, 1.0]
        y_const = [2.0, 3.0, 4.0]
        slope, intercept, r2 = calculate_linear_regression(x_const, y_const)
        self.assertEqual(slope, 0.0)
        self.assertEqual(r2, 0.0)
        
    def test_analyze_playlist_data(self):
        # Prepare small mock dataset
        # Video 0: 100 views, Video 1: 50 views, Video 2: 20 views
        playlist_meta = {
            "id": "test_id",
            "title": "Test Course",
            "category": "Testing",
            "expected_retention": "Medium",
            "incentive_group": "Aspirational"
        }
        videos = [
            {"id": "v1", "title": "Vid 1", "position": 0, "duration_seconds": 60, "view_count": 100},
            {"id": "v2", "title": "Vid 2", "position": 1, "duration_seconds": 120, "view_count": 50},
            {"id": "v3", "title": "Vid 3", "position": 2, "duration_seconds": 180, "view_count": 20}
        ]
        
        analysis = analyze_playlist_data(playlist_meta, videos)
        
        # Check overall metrics
        metrics = analysis["metrics"]
        self.assertEqual(metrics["total_videos"], 3)
        self.assertEqual(metrics["total_views"], 170)
        self.assertEqual(metrics["avg_duration_seconds"], 120.0)
        
        # First-video dropoff: (100 - 50) / 100 * 100 = 50.0%
        self.assertEqual(metrics["first_video_dropoff_percentage"], 50.0)
        
        # Overall retention: 20 / 100 * 100 = 20.0%
        self.assertEqual(metrics["overall_retention_percentage"], 20.0)
        
        # Half-life: first index where retention < 50%.
        # Video 0: 100%
        # Video 1: 50% (not < 50%)
        # Video 2: 20% (< 50%) -> index 2
        self.assertEqual(metrics["half_life"], 2)
        
        # Check individual video analysis
        vid_stats = analysis["videos"]
        self.assertEqual(vid_stats[0]["retention_percentage"], 100.0)
        self.assertEqual(vid_stats[0]["local_dropoff_percentage"], 0.0)
        
        self.assertEqual(vid_stats[1]["retention_percentage"], 50.0)
        self.assertEqual(vid_stats[1]["local_dropoff_percentage"], 50.0) # (100 - 50) / 100
        
        self.assertEqual(vid_stats[2]["retention_percentage"], 20.0)
        self.assertEqual(vid_stats[2]["local_dropoff_percentage"], 60.0) # (50 - 20) / 50
        
    def test_fit_curves(self):
        # Test curve fitting outputs structure and values
        positions = [0, 1, 2, 3]
        views = [1000, 500, 250, 125] # perfect exponential decay: views_i = 1000 * 0.5^i
        
        fitting = fit_curves(positions, views)
        
        # Check keys
        self.assertIn("exponential", fitting)
        self.assertIn("power", fitting)
        
        # For perfect exponential decay, exponential R2 should be very close to 1.0
        self.assertGreater(fitting["exponential"]["r2"], 0.99)
        # Power law should also fit but with a lower R2
        self.assertGreater(fitting["exponential"]["r2"], fitting["power"]["r2"])
        
        # Decay constant 'b' for exp: views_i = views_0 * e^(-b * i)
        # 500 = 1000 * e^(-b * 1) => 0.5 = e^(-b) => b = ln(2) = 0.6931
        self.assertAlmostEqual(fitting["exponential"]["b"], math.log(2), places=3)

if __name__ == "__main__":
    unittest.main()
