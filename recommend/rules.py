# conceptual rule engine
RECOMMENDATION_RULES = {
    "vehicle_exhaust": "Suggest temporary heavy-vehicle restriction on identified corridor; flag for increased public transit frequency",
    "road_dust": "Suggest water-sprinkling/dust-suppression on flagged road segments",
    "waste_burning": "Suggest notification to municipal ward sanitation contact for the zone",
    "industrial_heavy": "Suggest compliance check reminder for registered units in the zone",
    "industrial_light": "Suggest compliance check reminder for registered units in the zone",
    "residential": "Suggest public advisory on clean-fuel usage during high-AQI windows"
}

def severity_rank(severity):
    ranks = {
        "Good": 0,
        "Satisfactory": 1,
        "Moderate": 2,
        "Poor": 3,
        "Very Poor": 4,
        "Severe": 5
    }
    return ranks.get(severity, 0)

def recommend_action(likely_source_profile, severity):
    if not likely_source_profile:
        return None
        
    # Get dominant source
    dominant = max(likely_source_profile, key=likely_source_profile.get)
    
    if severity_rank(severity) < severity_rank("Poor"):
        return None # no action needed below this threshold
        
    return RECOMMENDATION_RULES.get(dominant)
