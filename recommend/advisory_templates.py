ADVISORY_TEMPLATES = {
    "en": {
        "schools": "AQI forecast: {severity} ({value}). Avoid outdoor assembly.",
        "hospitals": "AQI forecast: {severity} ({value}). Expect possible respiratory cases.",
        "outdoor_workers": "AQI forecast: {severity} ({value}). N95 mask recommended.",
        "general": "AQI forecast: {severity} ({value}). Stay indoors if you experience breathing difficulty."
    },
    "hi": {
        "schools": "वायु गुणवत्ता पूर्वानुमान: {severity} ({value})। बाहरी सभा से बचें।",
        "hospitals": "वायु गुणवत्ता पूर्वानुमान: {severity} ({value})। श्वसन संबंधी मामलों की संभावना।",
        "outdoor_workers": "वायु गुणवत्ता पूर्वानुमान: {severity} ({value})। N95 मास्क की सलाह।",
        "general": "वायु गुणवत्ता पूर्वानुमान: {severity} ({value})। सांस लेने में तकलीफ होने पर घर के अंदर रहें।"
    }
}

def get_advisories(severity, value, language="en"):
    templates = ADVISORY_TEMPLATES.get(language, ADVISORY_TEMPLATES["en"])
    
    return {
        audience: text.format(severity=severity, value=value)
        for audience, text in templates.items()
    }
