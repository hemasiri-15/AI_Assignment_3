"""
india_cities.py — Indian Cities Road Distance Graph
AI Assignment 3 | Uniform Cost Search (Dijkstra)

Road distances in kilometres between major Indian cities.
Source: Approximate real road distances from open sources.

Graph is undirected — distance A→B == distance B→A.
"""

# Adjacency list: {city: [(neighbour, distance_km), ...]}
INDIA_ROAD_GRAPH = {
    "Delhi": [
        ("Jaipur", 281),
        ("Agra", 233),
        ("Chandigarh", 274),
        ("Lucknow", 555),
        ("Amritsar", 452),
        ("Haridwar", 214),
    ],
    "Jaipur": [
        ("Delhi", 281),
        ("Agra", 238),
        ("Jodhpur", 343),
        ("Udaipur", 421),
        ("Ahmedabad", 671),
        ("Ajmer", 135),
    ],
    "Agra": [
        ("Delhi", 233),
        ("Jaipur", 238),
        ("Lucknow", 363),
        ("Gwalior", 119),
        ("Kanpur", 298),
    ],
    "Lucknow": [
        ("Delhi", 555),
        ("Agra", 363),
        ("Kanpur", 87),
        ("Varanasi", 286),
        ("Allahabad", 200),
        ("Patna", 528),
    ],
    "Chandigarh": [
        ("Delhi", 274),
        ("Amritsar", 229),
        ("Shimla", 117),
        ("Jammu", 190),
    ],
    "Amritsar": [
        ("Delhi", 452),
        ("Chandigarh", 229),
        ("Jammu", 209),
        ("Ludhiana", 141),
    ],
    "Jammu": [
        ("Amritsar", 209),
        ("Chandigarh", 190),
        ("Srinagar", 258),
    ],
    "Srinagar": [
        ("Jammu", 258),
    ],
    "Shimla": [
        ("Chandigarh", 117),
        ("Manali", 280),
    ],
    "Manali": [
        ("Shimla", 280),
    ],
    "Haridwar": [
        ("Delhi", 214),
        ("Dehradun", 54),
        ("Rishikesh", 24),
    ],
    "Dehradun": [
        ("Haridwar", 54),
        ("Rishikesh", 43),
    ],
    "Rishikesh": [
        ("Haridwar", 24),
        ("Dehradun", 43),
    ],
    "Varanasi": [
        ("Lucknow", 286),
        ("Allahabad", 121),
        ("Patna", 246),
        ("Gaya", 247),
    ],
    "Allahabad": [
        ("Lucknow", 200),
        ("Varanasi", 121),
        ("Kanpur", 193),
        ("Gwalior", 391),
    ],
    "Kanpur": [
        ("Lucknow", 87),
        ("Agra", 298),
        ("Allahabad", 193),
    ],
    "Patna": [
        ("Lucknow", 528),
        ("Varanasi", 246),
        ("Gaya", 100),
        ("Kolkata", 600),
        ("Ranchi", 330),
    ],
    "Gaya": [
        ("Patna", 100),
        ("Varanasi", 247),
        ("Ranchi", 260),
        ("Kolkata", 497),
    ],
    "Kolkata": [
        ("Patna", 600),
        ("Gaya", 497),
        ("Bhubaneswar", 441),
        ("Ranchi", 400),
        ("Siliguri", 569),
    ],
    "Bhubaneswar": [
        ("Kolkata", 441),
        ("Visakhapatnam", 443),
        ("Raipur", 441),
    ],
    "Ranchi": [
        ("Patna", 330),
        ("Gaya", 260),
        ("Kolkata", 400),
        ("Raipur", 378),
    ],
    "Siliguri": [
        ("Kolkata", 569),
        ("Guwahati", 435),
    ],
    "Guwahati": [
        ("Siliguri", 435),
    ],
    "Gwalior": [
        ("Agra", 119),
        ("Allahabad", 391),
        ("Bhopal", 423),
        ("Jhansi", 101),
    ],
    "Jhansi": [
        ("Gwalior", 101),
        ("Bhopal", 323),
        ("Nagpur", 518),
    ],
    "Bhopal": [
        ("Gwalior", 423),
        ("Jhansi", 323),
        ("Nagpur", 349),
        ("Indore", 193),
        ("Jabalpur", 295),
    ],
    "Indore": [
        ("Bhopal", 193),
        ("Ahmedabad", 395),
        ("Mumbai", 597),
        ("Ujjain", 55),
    ],
    "Ujjain": [
        ("Indore", 55),
        ("Bhopal", 183),
    ],
    "Jabalpur": [
        ("Bhopal", 295),
        ("Nagpur", 304),
        ("Raipur", 323),
    ],
    "Nagpur": [
        ("Bhopal", 349),
        ("Jhansi", 518),
        ("Jabalpur", 304),
        ("Hyderabad", 503),
        ("Mumbai", 836),
        ("Raipur", 292),
    ],
    "Raipur": [
        ("Nagpur", 292),
        ("Jabalpur", 323),
        ("Bhubaneswar", 441),
        ("Ranchi", 378),
        ("Visakhapatnam", 536),
    ],
    "Ahmedabad": [
        ("Jaipur", 671),
        ("Indore", 395),
        ("Mumbai", 524),
        ("Surat", 265),
        ("Vadodara", 113),
        ("Jodhpur", 485),
    ],
    "Vadodara": [
        ("Ahmedabad", 113),
        ("Surat", 154),
        ("Mumbai", 421),
    ],
    "Surat": [
        ("Ahmedabad", 265),
        ("Vadodara", 154),
        ("Mumbai", 284),
    ],
    "Mumbai": [
        ("Ahmedabad", 524),
        ("Surat", 284),
        ("Vadodara", 421),
        ("Pune", 149),
        ("Nagpur", 836),
        ("Goa", 593),
        ("Hyderabad", 711),
    ],
    "Pune": [
        ("Mumbai", 149),
        ("Hyderabad", 559),
        ("Goa", 455),
        ("Solapur", 244),
    ],
    "Solapur": [
        ("Pune", 244),
        ("Hyderabad", 319),
    ],
    "Goa": [
        ("Mumbai", 593),
        ("Pune", 455),
        ("Mangalore", 352),
        ("Bangalore", 562),
    ],
    "Hyderabad": [
        ("Nagpur", 503),
        ("Mumbai", 711),
        ("Pune", 559),
        ("Solapur", 319),
        ("Bangalore", 570),
        ("Chennai", 627),
        ("Visakhapatnam", 625),
    ],
    "Visakhapatnam": [
        ("Bhubaneswar", 443),
        ("Raipur", 536),
        ("Hyderabad", 625),
        ("Chennai", 791),
    ],
    "Bangalore": [
        ("Hyderabad", 570),
        ("Chennai", 346),
        ("Mysore", 143),
        ("Goa", 562),
        ("Mangalore", 352),
        ("Coimbatore", 363),
        ("Kochi", 540),
    ],
    "Mysore": [
        ("Bangalore", 143),
        ("Coimbatore", 214),
        ("Mangalore", 253),
    ],
    "Mangalore": [
        ("Goa", 352),
        ("Bangalore", 352),
        ("Mysore", 253),
        ("Kochi", 303),
    ],
    "Chennai": [
        ("Hyderabad", 627),
        ("Bangalore", 346),
        ("Coimbatore", 497),
        ("Madurai", 461),
        ("Visakhapatnam", 791),
        ("Tirupati", 137),
    ],
    "Tirupati": [
        ("Chennai", 137),
        ("Hyderabad", 561),
    ],
    "Coimbatore": [
        ("Bangalore", 363),
        ("Chennai", 497),
        ("Mysore", 214),
        ("Kochi", 186),
        ("Madurai", 213),
    ],
    "Madurai": [
        ("Chennai", 461),
        ("Coimbatore", 213),
        ("Kochi", 208),
        ("Trivandrum", 219),
    ],
    "Kochi": [
        ("Bangalore", 540),
        ("Mangalore", 303),
        ("Coimbatore", 186),
        ("Madurai", 208),
        ("Trivandrum", 205),
    ],
    "Trivandrum": [
        ("Kochi", 205),
        ("Madurai", 219),
    ],
    "Jodhpur": [
        ("Jaipur", 343),
        ("Ahmedabad", 485),
        ("Udaipur", 262),
        ("Ajmer", 203),
    ],
    "Udaipur": [
        ("Jaipur", 421),
        ("Jodhpur", 262),
        ("Ahmedabad", 262),
        ("Ajmer", 280),
    ],
    "Ajmer": [
        ("Jaipur", 135),
        ("Jodhpur", 203),
        ("Udaipur", 280),
    ],
    "Ludhiana": [
        ("Amritsar", 141),
        ("Chandigarh", 95),
    ],
}


def get_all_cities():
    """Return sorted list of all cities in the graph."""
    return sorted(INDIA_ROAD_GRAPH.keys())


def get_neighbours(city):
    """Return list of (neighbour, distance) for a city."""
    return INDIA_ROAD_GRAPH.get(city, [])
