# dictionary with programming language as key and list of repositories and file extensions
LANGUAGE_DATA = {
    "GAP": {
        "extensions": [".g", ".gd", ".gi"],
        "repository": ["repository_names"]
    },
    "PYTHON": {
        "extensions": [".py"],
        "repository": ["repository_names"]
    },
    "JAVA": {
        "extensions": [".java"],
        "repository": ["repository_names"]
    },
    "JAVASCRIPT": {
        "extensions": [".js"],
        "repository": ["repository_names"]
    },
    "TYPESCRIPT": {
        "extensions": [".ts"],
        "repository": ["repository_names"]
    },
    "GO": {
        "extensions": [".go"],
        "repository": ["repository_names"]
    },
    "PHP": {
        "extensions": [".php"],
        "repository": ["repository_names"]
    },
    "RUBY": {
        "extensions": [".rb"],
        "repository": ["repository_names"]
    }

    # Add more language entries as needed
}

# Acknowledgement: Status codes are taken from https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml      
HTTP_STATUS_CODES = {"SUCCESS": 200, "FORBIDDEN": 403, "TOO_MANY_REQUESTS": 429}

# Acknowledgement: County codes are taken from https://www.ssa.gov/international/coc-docs/states.html 
US_COUNTY_CODES = {"AL":"ALABAMA",
"AK":"ALASKA",
"AS":"AMERICAN SAMOA",
"AZ":"ARIZONA",
"AR":"ARKANSAS",
"CA":"CALIFORNIA",
"CO":"COLORADO",
"CT":"CONNECTICUT",
"DE":"DELAWARE",
"DC":"DISTRICT OF COLUMBIA",	
"FL":"FLORIDA",
"GA":"GEORGIA",
"GU":"GUAM",
"HI":"HAWAII",	
"ID":"IDAHO",
"IL":"ILLINOIS",	
"IN":"INDIANA",
"IA":"IOWA",
"KS":"KANSAS",	
"KY":"KENTUCKY",	
"LA":"LOUISIANA",
"ME":"MAINE",
"MD":"MARYLAND",	
"MA":"MASSACHUSETTS",	
"MI":"MICHIGAN",	
"MN":"MINNESOTA",	
"MS":"MISSISSIPPI",	
"MO":"MISSOURI",	
"MT":"MONTANA",	
"NE":"NEBRASKA",	
"NV":"NEVADA",	
"NH":"NEW HAMPSHIRE",	
"NJ":"NEW JERSEY",	
"NM":"NEW MEXICO",	
"NY":"NEW YORK",	
"NC":"NORTH CAROLINA",	
"ND":"NORTH DAKOTA",	
"MP":"NORTHERN MARIANA IS",	
"OH":"OHIO",	
"OK":"OKLAHOMA",	
"OR":"OREGON",	
"PA":"PENNSYLVANIA",	
"PR":"PUERTO RICO",	
"RI":"RHODE ISLAND",	
"SC":"SOUTH CAROLINA",	
"SD":"SOUTH DAKOTA",	
"TN":"TENNESSEE",	
"TX":"TEXAS",	
"UT":"UTAH",	
"VT":"VERMONT",	
"VA":"VIRGINIA",	
"VI":"VIRGIN ISLANDS",	
"WA":"WASHINGTON",	
"WV":"WEST VIRGINIA",	
"WI":"WISCONSIN",	
"WY":"WYOMING"}

US_COUNTRY_NAME = "United States"