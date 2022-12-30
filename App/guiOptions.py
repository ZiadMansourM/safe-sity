
options = {
    "Giza": {
        "6 October": [
            "Street 43",
            "Street 44",     
        ],
        "Dokki": [
            "Street 50",
            "Street 3",
        ]
    },
    "Cairo": {
        "Fifth Settlement": [
            "Street 1",
            "Street 2",
        ],
        "Nasr City": [
            "Street 22",
            "Street 4",
        ]
    }
}

governments = list(options.keys())
cities = list(options[governments[0]].keys())
streets = list(options[governments[0]][cities[0]])