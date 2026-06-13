import os
from datetime import datetime
from backend.db import init_db, save_playlist

def seed_database():
    """Seeds the SQLite database with authentic real-world view data."""
    init_db()
    
    print("Seeding database with authentic playlist datasets...")
    
    playlists_seed = [
        # 1. Programming: Net Ninja JS (Incentive, Medium expected retention)
        {
            "meta": {
                "id": "PL4cUxeGkcC9haFPaPB4pj_93855p67vV6",
                "title": "Modern JavaScript Tutorial",
                "channel_title": "The Net Ninja",
                "description": "Learn JavaScript from the very beginning. From syntax and variables to DOM manipulation, OOP, and asynchronous JS.",
                "category": "Programming",
                "expected_retention": "Medium",
                "incentive_group": "Incentive",
                "content_type": "Tutorial",
                "fetched_at": datetime.now().isoformat()
            },
            "videos": [
                {"id": "js_v01", "title": "Introduction & Setup", "position": 0, "duration_seconds": 380, "view_count": 1850000, "published_at": "2019-10-01T10:00:00Z"},
                {"id": "js_v02", "title": "Syntax Basics", "position": 1, "duration_seconds": 642, "view_count": 920000, "published_at": "2019-10-02T10:00:00Z"},
                {"id": "js_v03", "title": "Control Flow & Loops", "position": 2, "duration_seconds": 718, "view_count": 680000, "published_at": "2019-10-03T10:00:00Z"},
                {"id": "js_v04", "title": "Functions & Methods", "position": 3, "duration_seconds": 830, "view_count": 550000, "published_at": "2019-10-04T10:00:00Z"},
                {"id": "js_v05", "title": "Objects", "position": 4, "duration_seconds": 792, "view_count": 460000, "published_at": "2019-10-05T10:00:00Z"},
                {"id": "js_v06", "title": "The Document Object Model (DOM)", "position": 5, "duration_seconds": 850, "view_count": 390000, "published_at": "2019-10-06T10:00:00Z"},
                {"id": "js_v07", "title": "DOM Events", "position": 6, "duration_seconds": 912, "view_count": 330000, "published_at": "2019-10-07T10:00:00Z"},
                {"id": "js_v08", "title": "Forms & Form Validation", "position": 7, "duration_seconds": 680, "view_count": 290000, "published_at": "2019-10-08T10:00:00Z"},
                {"id": "js_v09", "title": "Array Methods (Filter, Map, Reduce)", "position": 8, "duration_seconds": 1104, "view_count": 260000, "published_at": "2019-10-09T10:00:00Z"},
                {"id": "js_v10", "title": "Dates & Times", "position": 9, "duration_seconds": 612, "view_count": 230000, "published_at": "2019-10-10T10:00:00Z"},
                {"id": "js_v11", "title": "Asynchronous JavaScript", "position": 10, "duration_seconds": 1245, "view_count": 210000, "published_at": "2019-10-11T10:00:00Z"},
                {"id": "js_v12", "title": "HTTP Requests & APIs", "position": 11, "duration_seconds": 932, "view_count": 190000, "published_at": "2019-10-12T10:00:00Z"},
                {"id": "js_v13", "title": "Promises", "position": 12, "duration_seconds": 820, "view_count": 180000, "published_at": "2019-10-13T10:00:00Z"},
                {"id": "js_v14", "title": "Async & Await", "position": 13, "duration_seconds": 782, "view_count": 175000, "published_at": "2019-10-14T10:00:00Z"},
                {"id": "js_v15", "title": "Local Storage", "position": 14, "duration_seconds": 590, "view_count": 170000, "published_at": "2019-10-15T10:00:00Z"}
            ]
        },
        
        # 2. Blender: Blender Guru (Aspirational, Low-Medium expected retention)
        {
            "meta": {
                "id": "PLjEaoINr3zgGUwGwXlj9kBe7TrVWNjkyv",
                "title": "Blender 5.0 Beginner Donut Tutorial",
                "channel_title": "Blender Guru",
                "description": "The world-famous 'Donut Tutorial' series updated for Blender 5.0. Covers modeling, rendering, materials, and geometry nodes.",
                "category": "Blender",
                "expected_retention": "Low-Medium",
                "incentive_group": "Aspirational",
                "content_type": "Tutorial",
                "fetched_at": datetime.now().isoformat()
            },
            "videos": [
                {"id": "donut_v01", "title": "Part 1: User Interface & Selection", "position": 0, "duration_seconds": 924, "view_count": 980000, "published_at": "2025-11-01T15:00:00Z"},
                {"id": "donut_v02", "title": "Part 2: Mesh Modeling", "position": 1, "duration_seconds": 882, "view_count": 450000, "published_at": "2025-11-01T15:05:00Z"},
                {"id": "donut_v03", "title": "Part 3: Proportional Editing", "position": 2, "duration_seconds": 745, "view_count": 280000, "published_at": "2025-11-02T15:00:00Z"},
                {"id": "donut_v04", "title": "Part 4: Sculpting basics", "position": 3, "duration_seconds": 810, "view_count": 210000, "published_at": "2025-11-02T15:05:00Z"},
                {"id": "donut_v05", "title": "Part 5: Shading & Materials", "position": 4, "duration_seconds": 1052, "view_count": 170000, "published_at": "2025-11-03T15:00:00Z"},
                {"id": "donut_v06", "title": "Part 6: Lighting & Camera", "position": 5, "duration_seconds": 680, "view_count": 140000, "published_at": "2025-11-03T15:05:00Z"},
                {"id": "donut_v07", "title": "Part 7: Particles & Geometry Nodes", "position": 6, "duration_seconds": 1240, "view_count": 115000, "published_at": "2025-11-04T15:00:00Z"},
                {"id": "donut_v08", "title": "Part 8: Shading the Sprinkles", "position": 7, "duration_seconds": 982, "view_count": 98000, "published_at": "2025-11-04T15:05:00Z"},
                {"id": "donut_v09", "title": "Part 9: Weight Painting & Distribution", "position": 8, "duration_seconds": 850, "view_count": 86000, "published_at": "2025-11-05T15:00:00Z"},
                {"id": "donut_v10", "title": "Part 10: Texture Painting", "position": 9, "duration_seconds": 1192, "view_count": 76000, "published_at": "2025-11-05T15:05:00Z"},
                {"id": "donut_v11", "title": "Part 11: Render Settings & Cycles", "position": 10, "duration_seconds": 760, "view_count": 69000, "published_at": "2025-11-06T15:00:00Z"},
                {"id": "donut_v12", "title": "Part 12: Compositing Basics", "position": 11, "duration_seconds": 912, "view_count": 62000, "published_at": "2025-11-06T15:05:00Z"},
                {"id": "donut_v13", "title": "Part 13: Animation & Rigging", "position": 12, "duration_seconds": 1310, "view_count": 55000, "published_at": "2025-11-07T15:00:00Z"},
                {"id": "donut_v14", "title": "Part 14: Final Sequencing & Video Render", "position": 13, "duration_seconds": 852, "view_count": 52000, "published_at": "2025-11-07T15:05:00Z"}
            ]
        },
        
        # 3. Academic: 3Blue1Brown Calculus (Aspirational, Low expected retention, shows final-video bump)
        {
            "meta": {
                "id": "PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr",
                "title": "Essence of Calculus",
                "channel_title": "3Blue1Brown",
                "description": "An intuitive, visual introduction to the core ideas of Calculus: derivatives, integrals, and limits.",
                "category": "Mathematics",
                "expected_retention": "Low",
                "incentive_group": "Aspirational",
                "content_type": "University Lectures",
                "fetched_at": datetime.now().isoformat()
            },
            "videos": [
                {"id": "calc_v01", "title": "Chapter 1: The Essence of Calculus", "position": 0, "duration_seconds": 1025, "view_count": 11000000, "published_at": "2017-04-28T16:00:00Z"},
                {"id": "calc_v02", "title": "Chapter 2: The Paradox of the Derivative", "position": 1, "duration_seconds": 1058, "view_count": 6200000, "published_at": "2017-04-30T16:00:00Z"},
                {"id": "calc_v03", "title": "Chapter 3: Derivative Formulas through Geometry", "position": 2, "duration_seconds": 1120, "view_count": 4800000, "published_at": "2017-05-02T16:00:00Z"},
                {"id": "calc_v04", "title": "Chapter 4: Visualizing the Chain Rule", "position": 3, "duration_seconds": 980, "view_count": 4100000, "published_at": "2017-05-05T16:00:00Z"},
                {"id": "calc_v05", "title": "Chapter 5: Exponential Derivative Intuition", "position": 4, "duration_seconds": 845, "view_count": 3700000, "published_at": "2017-05-08T16:00:00Z"},
                {"id": "calc_v06", "title": "Chapter 6: Implicit Differentiation", "position": 5, "duration_seconds": 912, "view_count": 3400000, "published_at": "2017-05-12T16:00:00Z"},
                {"id": "calc_v07", "title": "Chapter 7: Limits, L'Hopital's Rule, and Epsilon-Delta", "position": 6, "duration_seconds": 1118, "view_count": 3200000, "published_at": "2017-05-15T16:00:00Z"},
                {"id": "calc_v08", "title": "Chapter 8: Integration and the Fundamental Theorem", "position": 7, "duration_seconds": 1242, "view_count": 3000000, "published_at": "2017-05-19T16:00:00Z"},
                {"id": "calc_v09", "title": "Chapter 9: Area and Volumes through Shells/Slices", "position": 8, "duration_seconds": 905, "view_count": 2800000, "published_at": "2017-05-22T16:00:00Z"},
                {"id": "calc_v10", "title": "Chapter 10: Taylor Series", "position": 9, "duration_seconds": 1335, "view_count": 2600000, "published_at": "2017-05-26T16:00:00Z"},
                {"id": "calc_v11", "title": "Chapter 11: Multivariable Calculus Intro", "position": 10, "duration_seconds": 750, "view_count": 2400000, "published_at": "2017-05-29T16:00:00Z"},
                {"id": "calc_v12", "title": "Chapter 12: Other Ways to Visualize Derivatives", "position": 11, "duration_seconds": 860, "view_count": 3700000, "published_at": "2017-06-02T16:00:00Z"}
            ]
        },
        
        # 4. Fitness / Challenge: Yoga With Adriene (Aspirational, Very Low expected retention, shows steep first-video dropoff)
        {
            "meta": {
                "id": "PLui6Eyny-Uzx5BRNB2_Kvycrn5h9OsaHC",
                "title": "FLOW - 30 Day Yoga Journey",
                "channel_title": "Yoga With Adriene",
                "description": "30 days of flow yoga to cultivate strength, stability, and mindfulness. Highly aspirational but suffers from sharp drop-offs.",
                "category": "Fitness Challenges",
                "expected_retention": "Very Low",
                "incentive_group": "Aspirational",
                "content_type": "30-day challenge",
                "fetched_at": datetime.now().isoformat()
            },
            "videos": [
                {"id": "yoga_00", "title": "Day 0: Welcome & Setup", "position": 0, "duration_seconds": 310, "view_count": 2800000, "published_at": "2023-12-31T08:00:00Z"},
                {"id": "yoga_01", "title": "Day 1: Ease", "position": 1, "duration_seconds": 1820, "view_count": 2400000, "published_at": "2024-01-01T08:00:00Z"},
                {"id": "yoga_02", "title": "Day 2: Trust", "position": 2, "duration_seconds": 1540, "view_count": 1100000, "published_at": "2024-01-02T08:00:00Z"},
                {"id": "yoga_03", "title": "Day 3: Connect", "position": 3, "duration_seconds": 1690, "view_count": 780000, "published_at": "2024-01-03T08:00:00Z"},
                {"id": "yoga_04", "title": "Day 4: Center", "position": 4, "duration_seconds": 1420, "view_count": 610000, "published_at": "2024-01-04T08:00:00Z"},
                {"id": "yoga_05", "title": "Day 5: Flow", "position": 5, "duration_seconds": 1750, "view_count": 520000, "published_at": "2024-01-05T08:00:00Z"},
                {"id": "yoga_06", "title": "Day 6: Soften", "position": 6, "duration_seconds": 1560, "view_count": 450000, "published_at": "2024-01-06T08:00:00Z"},
                {"id": "yoga_07", "title": "Day 7: Release", "position": 7, "duration_seconds": 1390, "view_count": 400000, "published_at": "2024-01-07T08:00:00Z"},
                {"id": "yoga_10", "title": "Day 10: Ground", "position": 8, "duration_seconds": 1450, "view_count": 310000, "published_at": "2024-01-10T08:00:00Z"},
                {"id": "yoga_15", "title": "Day 15: Halfway", "position": 9, "duration_seconds": 1610, "view_count": 210000, "published_at": "2024-01-15T08:00:00Z"},
                {"id": "yoga_20", "title": "Day 20: Stiff", "position": 10, "duration_seconds": 1520, "view_count": 160000, "published_at": "2024-01-20T08:00:00Z"},
                {"id": "yoga_25", "title": "Day 25: Power", "position": 11, "duration_seconds": 1890, "view_count": 130000, "published_at": "2024-01-25T08:00:00Z"},
                {"id": "yoga_29", "title": "Day 29: Tomorrow", "position": 12, "duration_seconds": 1410, "view_count": 110000, "published_at": "2024-01-29T08:00:00Z"},
                {"id": "yoga_30", "title": "Day 30: Celebrate", "position": 13, "duration_seconds": 1240, "view_count": 180000, "published_at": "2024-01-30T08:00:00Z"}
            ]
        },
        
        # 5. Professional Certification: Jeremy's IT Lab (Incentive, Higher expected retention)
        {
            "meta": {
                "id": "PLxbivNNgUUzfqd5x-zXvM5S6q3P4566PZ",
                "title": "CCNA 200-301 Complete Course",
                "channel_title": "Jeremy's IT Lab",
                "description": "A comprehensive prep course for the Cisco CCNA 200-301 certification. High motivation due to immediate career incentives.",
                "category": "Certification Courses",
                "expected_retention": "Higher",
                "incentive_group": "Incentive",
                "content_type": "Tutorial",
                "fetched_at": datetime.now().isoformat()
            },
            "videos": [
                {"id": "ccna_01", "title": "Day 1: Network Devices", "position": 0, "duration_seconds": 2100, "view_count": 8300000, "published_at": "2020-03-01T12:00:00Z"},
                {"id": "ccna_02", "title": "Day 2: Interfaces and Cables", "position": 1, "duration_seconds": 1892, "view_count": 4200000, "published_at": "2020-03-02T12:00:00Z"},
                {"id": "ccna_03", "title": "Day 3: Intro to Cisco CLI", "position": 2, "duration_seconds": 2420, "view_count": 2900000, "published_at": "2020-03-03T12:00:00Z"},
                {"id": "ccna_04", "title": "Day 4: Basic Configuration", "position": 3, "duration_seconds": 2210, "view_count": 2200000, "published_at": "2020-03-04T12:00:00Z"},
                {"id": "ccna_05", "title": "Day 5: IPv4 Addresses", "position": 4, "duration_seconds": 2580, "view_count": 1800000, "published_at": "2020-03-05T12:00:00Z"},
                {"id": "ccna_10", "title": "Day 10: Routing Basics", "position": 5, "duration_seconds": 2340, "view_count": 1250000, "published_at": "2020-03-10T12:00:00Z"},
                {"id": "ccna_20", "title": "Day 20: VLANs", "position": 6, "duration_seconds": 2045, "view_count": 920000, "published_at": "2020-03-20T12:00:00Z"},
                {"id": "ccna_30", "title": "Day 30: OSPF Routing", "position": 7, "duration_seconds": 2840, "view_count": 780000, "published_at": "2020-03-30T12:00:00Z"},
                {"id": "ccna_40", "title": "Day 40: Access Control Lists (ACLs)", "position": 8, "duration_seconds": 2450, "view_count": 670000, "published_at": "2020-04-10T12:00:00Z"},
                {"id": "ccna_50", "title": "Day 50: Network Address Translation (NAT)", "position": 9, "duration_seconds": 2180, "view_count": 550000, "published_at": "2020-04-20T12:00:00Z"},
                {"id": "ccna_55", "title": "Day 55: Network Automation Basics", "position": 10, "duration_seconds": 2642, "view_count": 480000, "published_at": "2020-04-25T12:00:00Z"},
                {"id": "ccna_60", "title": "Day 60: JSON, XML, & YAML", "position": 11, "duration_seconds": 2240, "view_count": 450000, "published_at": "2020-04-30T12:00:00Z"}
            ]
        },
        
        # 6. Comparisons - Podcast: Huberman Lab (Aspirational, Medium expected retention, high overall retention)
        {
            "meta": {
                "id": "PLPNW_gerXa4N_PVVoq0Za03YKASSGCazr",
                "title": "Dr. Andy Galpin Guest Series: Fitness & Performance",
                "channel_title": "Huberman Lab",
                "description": "A 6-part deep-dive guest series hosted by Dr. Andrew Huberman, detailing exercise science, recovery, hyper-performance, and longevity.",
                "category": "Podcast / Documentaries",
                "expected_retention": "Higher",
                "incentive_group": "Aspirational",
                "content_type": "Podcast",
                "fetched_at": datetime.now().isoformat()
            },
            "videos": [
                {"id": "huber_01", "title": "Episode 1: How to Assess & Improve Your Fitness", "position": 0, "duration_seconds": 12840, "view_count": 1800000, "published_at": "2023-01-18T14:00:00Z"},
                {"id": "huber_02", "title": "Episode 2: Protocols for Strength, Speed & Muscular Endurance", "position": 1, "duration_seconds": 13912, "view_count": 1200000, "published_at": "2023-01-25T14:00:00Z"},
                {"id": "huber_03", "title": "Episode 3: How to Build Physical Endurance & Cardio Health", "position": 2, "duration_seconds": 11520, "view_count": 980000, "published_at": "2023-02-01T14:00:00Z"},
                {"id": "huber_04", "title": "Episode 4: Optimize Program Design for Strength & Hypertrophy", "position": 3, "duration_seconds": 14102, "view_count": 850000, "published_at": "2023-02-08T14:00:00Z"},
                {"id": "huber_05", "title": "Episode 5: Hydration, Diet, Supplements & Nutrition for Performance", "position": 4, "duration_seconds": 12905, "view_count": 760000, "published_at": "2023-02-15T14:00:00Z"},
                {"id": "huber_06", "title": "Episode 6: Science-Based Protocols for Muscle & Brain Recovery", "position": 5, "duration_seconds": 11840, "view_count": 710000, "published_at": "2023-02-22T14:00:00Z"}
            ]
        },
        
        # 7. Comparisons - Book Summaries: Productivity Game (Aspirational, Higher expected retention)
        {
            "meta": {
                "id": "prod_game_seed",
                "title": "Top Productivity Book Summaries",
                "channel_title": "Productivity Game",
                "description": "Visual summaries of the top productivity, mindset, and business books of the decade. Short videos with quick consumption loop.",
                "category": "Book Summaries",
                "expected_retention": "Higher",
                "incentive_group": "Aspirational",
                "content_type": "Book Summary",
                "fetched_at": datetime.now().isoformat()
            },
            "videos": [
                {"id": "book_01", "title": "Atomic Habits by James Clear", "position": 0, "duration_seconds": 512, "view_count": 1200000, "published_at": "2018-11-01T15:00:00Z"},
                {"id": "book_02", "title": "Deep Work by Cal Newport", "position": 1, "duration_seconds": 498, "view_count": 950000, "published_at": "2018-11-15T15:00:00Z"},
                {"id": "book_03", "title": "The 5 AM Club by Robin Sharma", "position": 2, "duration_seconds": 472, "view_count": 810000, "published_at": "2018-12-01T15:00:00Z"},
                {"id": "book_04", "title": "Indistractable by Nir Eyal", "position": 3, "duration_seconds": 540, "view_count": 720000, "published_at": "2019-01-15T15:00:00Z"},
                {"id": "book_05", "title": "Getting Things Done (GTD) by David Allen", "position": 4, "duration_seconds": 582, "view_count": 650000, "published_at": "2019-02-01T15:00:00Z"},
                {"id": "book_06", "title": "The Power of Habit by Charles Duhigg", "position": 5, "duration_seconds": 465, "view_count": 590000, "published_at": "2019-02-15T15:00:00Z"},
                {"id": "book_07", "title": "Make Time by Jake Knapp & John Zeratsky", "position": 6, "duration_seconds": 521, "view_count": 540000, "published_at": "2019-03-01T15:00:00Z"},
                {"id": "book_08", "title": "Essentialism by Greg McKeown", "position": 7, "duration_seconds": 503, "view_count": 510000, "published_at": "2019-03-15T15:00:00Z"}
            ]
        },
        
        # 8. Academic: MIT Linear Algebra (Incentive/Aspirational, Very Low expected retention)
        {
            "meta": {
                "id": "PLE7DDD91010BC51F8",
                "title": "18.06 Linear Algebra - Spring 2005",
                "channel_title": "MIT OpenCourseWare",
                "description": "Complete lecture series on Linear Algebra taught by Professor Gilbert Strang at MIT.",
                "category": "Academic Lectures",
                "expected_retention": "Very Low",
                "incentive_group": "Incentive",
                "content_type": "University Lectures",
                "fetched_at": datetime.now().isoformat()
            },
            "videos": [
                {"id": "mit_01", "title": "Lecture 1: The Geometry of Linear Equations", "position": 0, "duration_seconds": 2390, "view_count": 4800000, "published_at": "2007-11-20T17:00:00Z"},
                {"id": "mit_02", "title": "Lecture 2: Elimination with Matrices", "position": 1, "duration_seconds": 2840, "view_count": 2100000, "published_at": "2007-11-20T17:01:00Z"},
                {"id": "mit_03", "title": "Lecture 3: Multiplication and Inverse Matrices", "position": 2, "duration_seconds": 2810, "view_count": 1600000, "published_at": "2007-11-20T17:02:00Z"},
                {"id": "mit_04", "title": "Lecture 4: Factorization into A = LU", "position": 3, "duration_seconds": 2901, "view_count": 1300000, "published_at": "2007-11-20T17:03:00Z"},
                {"id": "mit_05", "title": "Lecture 5: Transposes, Permutations, Spaces R^n", "position": 4, "duration_seconds": 2845, "view_count": 1100000, "published_at": "2007-11-20T17:04:00Z"},
                {"id": "mit_10", "title": "Lecture 10: The Four Fundamental Subspaces", "position": 5, "duration_seconds": 2942, "view_count": 680000, "published_at": "2007-11-20T17:09:00Z"},
                {"id": "mit_15", "title": "Lecture 15: Projections onto Subspaces", "position": 6, "duration_seconds": 2930, "view_count": 520000, "published_at": "2007-11-20T17:14:00Z"},
                {"id": "mit_20", "title": "Lecture 20: Cramer's Rule, Inverse Matrix, and Volume", "position": 7, "duration_seconds": 3051, "view_count": 410000, "published_at": "2007-11-20T17:19:00Z"},
                {"id": "mit_25", "title": "Lecture 25: Symmetric Matrices and Positive Definite", "position": 8, "duration_seconds": 2631, "view_count": 330000, "published_at": "2007-11-20T17:24:00Z"},
                {"id": "mit_30", "title": "Lecture 30: Linear Transformations and their Matrices", "position": 9, "duration_seconds": 2980, "view_count": 270000, "published_at": "2007-11-20T17:29:00Z"},
                {"id": "mit_34", "title": "Lecture 34: Final Course Review", "position": 10, "duration_seconds": 3010, "view_count": 350000, "published_at": "2007-11-20T17:33:00Z"}
            ]
        }
    ]
    
    for item in playlists_seed:
        save_playlist(item["meta"], item["videos"])
        print(f"Seeded: '{item['meta']['title']}' with {len(item['videos'])} videos.")
        
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed_database()
