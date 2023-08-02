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