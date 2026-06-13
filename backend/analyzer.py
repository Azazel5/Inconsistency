import math

def calculate_linear_regression(x, y):
    """
    Computes simple linear regression coefficients for y = m * x + c 
    and returns (slope, intercept, r_squared).
    """
    n = len(x)
    if n < 2:
        return 0.0, 0.0, 0.0
        
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    num = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    den = sum((x[i] - mean_x) ** 2 for i in range(n))
    
    if den == 0:
        return 0.0, mean_y, 0.0
        
    slope = num / den
    intercept = mean_y - slope * mean_x
    
    # Calculate R-squared
    ss_tot = sum((y[i] - mean_y) ** 2 for i in range(n))
    ss_res = sum((y[i] - (slope * x[i] + intercept)) ** 2 for i in range(n))
    
    r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
    return slope, intercept, r_squared

def fit_curves(positions, views):
    """
    Fits the views data to Exponential and Power-law models.
    Returns:
        dict: Fitting results for both models including coefficients, R2, and curves.
    """
    if not views or len(views) < 2 or views[0] == 0:
        return {
            "exponential": {"a": 0, "b": 0, "r2": 0, "fitted_curve": []},
            "power": {"a": 0, "b": 0, "r2": 0, "fitted_curve": []}
        }
        
    v1 = views[0]
    
    # We fit retention: R_i = views_i / views_1
    retention = [v / v1 for v in views]
    
    # Prepare data points for regression, skipping indices where view count <= 0 to avoid log issues
    exp_x = []
    exp_y = []
    power_x = []
    power_y = []
    
    for i, r in enumerate(retention):
        if r <= 0:
            continue
        # Exponential: ln(R_i) = ln(a) - b * i
        exp_x.append(float(i))
        exp_y.append(math.log(r))
        
        # Power Law: ln(R_i) = ln(a) - b * ln(i + 1)
        power_x.append(math.log(float(i + 1)))
        power_y.append(math.log(r))
        
    # Fit Exponential
    exp_slope, exp_intercept, exp_r2 = calculate_linear_regression(exp_x, exp_y)
    exp_a = math.exp(exp_intercept)
    exp_b = -exp_slope  # decay constant
    
    # Fit Power Law
    pow_slope, pow_intercept, pow_r2 = calculate_linear_regression(power_x, power_y)
    pow_a = math.exp(pow_intercept)
    pow_b = -pow_slope  # power exponent
    
    # Generate fitted curves
    exp_fitted = []
    pow_fitted = []
    for i in range(len(views)):
        # exp_y_fit = exp_a * e^(-exp_b * i)
        exp_val = exp_a * math.exp(-exp_b * i)
        exp_fitted.append(min(1.0, exp_val) * 100) # percentage
        
        # pow_y_fit = pow_a * (i+1)^(-pow_b)
        pow_val = pow_a * ((i + 1) ** -pow_b)
        pow_fitted.append(min(1.0, pow_val) * 100) # percentage
        
    return {
        "exponential": {
            "a": round(exp_a, 4),
            "b": round(exp_b, 4),
            "r2": round(exp_r2, 4),
            "fitted_curve": exp_fitted
        },
        "power": {
            "a": round(pow_a, 4),
            "b": round(pow_b, 4),
            "r2": round(pow_r2, 4),
            "fitted_curve": pow_fitted
        }
    }

def analyze_playlist_data(playlist_meta, videos):
    """
    Performs complete analysis on a list of videos in a playlist.
    Returns:
        dict: Rich analysis summary with individual video stats and comparison curves.
    """
    if not videos:
        return {
            "metadata": playlist_meta,
            "videos": [],
            "metrics": {
                "total_videos": 0,
                "first_video_dropoff": 0.0,
                "overall_retention": 0.0,
                "half_life": -1,
                "avg_duration_seconds": 0.0,
                "total_views": 0
            },
            "fitting": {}
        }
        
    # Ensure videos are sorted by position
    sorted_videos = sorted(videos, key=lambda v: v["position"])
    
    views = [v["view_count"] for v in sorted_videos]
    positions = [v["position"] for v in sorted_videos]
    v1 = views[0] if views else 0
    
    analyzed_videos = []
    half_life_index = -1
    
    for i, v in enumerate(sorted_videos):
        # 1. Retention percentage relative to video 1
        retention = (v["view_count"] / v1 * 100.0) if v1 > 0 else 0.0
        
        # Track half-life
        if retention < 50.0 and half_life_index == -1:
            half_life_index = v["position"]
            
        # 2. Local dropoff from the previous video
        if i == 0:
            local_dropoff = 0.0
        else:
            prev_views = sorted_videos[i-1]["view_count"]
            local_dropoff = ((prev_views - v["view_count"]) / prev_views * 100.0) if prev_views > 0 else 0.0
            
        analyzed_videos.append({
            "id": v["id"],
            "title": v["title"],
            "position": v["position"],
            "duration_seconds": v.get("duration_seconds", 0),
            "view_count": v["view_count"],
            "published_at": v.get("published_at"),
            "retention_percentage": round(retention, 2),
            "local_dropoff_percentage": round(local_dropoff, 2)
        })
        
    # Calculate overall metrics
    total_videos = len(sorted_videos)
    total_views = sum(views)
    avg_duration = sum(v.get("duration_seconds", 0) for v in sorted_videos) / total_videos
    
    first_video_dropoff = 0.0
    if total_videos > 1:
        first_video_dropoff = ((views[0] - views[1]) / views[0] * 100.0) if views[0] > 0 else 0.0
        
    overall_retention = (views[-1] / views[0] * 100.0) if views[0] > 0 else 0.0
    
    # Fit curves
    fitting = fit_curves(positions, views)
    
    # Determine best fit model
    exp_r2 = fitting["exponential"]["r2"]
    pow_r2 = fitting["power"]["r2"]
    if exp_r2 == 0 and pow_r2 == 0:
        best_fit = "None"
    elif pow_r2 >= exp_r2:
        best_fit = "Power Law"
    else:
        best_fit = "Exponential"
        
    return {
        "metadata": playlist_meta,
        "videos": analyzed_videos,
        "metrics": {
            "total_videos": total_videos,
            "total_views": total_views,
            "avg_duration_seconds": round(avg_duration, 1),
            "first_video_dropoff_percentage": round(first_video_dropoff, 2),
            "overall_retention_percentage": round(overall_retention, 2),
            "half_life": half_life_index,
            "best_fit_model": best_fit
        },
        "fitting": fitting
    }

def aggregate_comparisons(playlists_data):
    """
    Aggregates retention curves and decay parameters grouped by:
    1. Category
    2. Incentive Group (Aspirational vs Incentive)
    3. Content Type
    
    Accepts:
        playlists_data: list of dicts returned by analyze_playlist_data
    """
    categories = {}
    incentives = {"Aspirational": [], "Incentive": []}
    content_types = {}
    
    # Helper to calculate average retention curve for a group of playlists
    def calculate_average_curve(playlists):
        if not playlists:
            return []
        # Find the maximum length of a playlist in this group (cap at e.g. 50 or average it)
        # We will average point-by-point. If a playlist is shorter, it stops contributing.
        # But to be mathematically sound, we take the average of all active playlists at each index.
        max_len = max(len(p["videos"]) for p in playlists)
        avg_curve = []
        
        for i in range(max_len):
            active_retentions = [
                p["videos"][i]["retention_percentage"] 
                for p in playlists 
                if i < len(p["videos"])
            ]
            if active_retentions:
                avg_curve.append(round(sum(active_retentions) / len(active_retentions), 2))
                
        return avg_curve

    for p in playlists_data:
        cat = p["metadata"].get("category", "General")
        inc = p["metadata"].get("incentive_group", "Aspirational")
        ct = p["metadata"].get("content_type", "Tutorial")
        
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)
        
        if inc in incentives:
            incentives[inc].append(p)
            
        if ct not in content_types:
            content_types[ct] = []
        content_types[ct].append(p)
        
    # Compile results
    results = {
        "categories": {
            name: {
                "avg_curve": calculate_average_curve(lists),
                "avg_first_dropoff": round(sum(l["metrics"]["first_video_dropoff_percentage"] for l in lists) / len(lists), 2),
                "avg_overall_retention": round(sum(l["metrics"]["overall_retention_percentage"] for l in lists) / len(lists), 2),
                "count": len(lists)
            }
            for name, lists in categories.items() if lists
        },
        "incentives": {
            name: {
                "avg_curve": calculate_average_curve(lists),
                "avg_first_dropoff": round(sum(l["metrics"]["first_video_dropoff_percentage"] for l in lists) / len(lists), 2),
                "avg_overall_retention": round(sum(l["metrics"]["overall_retention_percentage"] for l in lists) / len(lists), 2),
                "count": len(lists)
            }
            for name, lists in incentives.items() if lists
        },
        "content_types": {
            name: {
                "avg_curve": calculate_average_curve(lists),
                "avg_first_dropoff": round(sum(l["metrics"]["first_video_dropoff_percentage"] for l in lists) / len(lists), 2),
                "avg_overall_retention": round(sum(l["metrics"]["overall_retention_percentage"] for l in lists) / len(lists), 2),
                "count": len(lists)
            }
            for name, lists in content_types.items() if lists
        }
    }
    
    return results
