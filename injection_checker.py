def is_sqli(data):
    sqli_patterns = ["'", "--", ";", "/", "/", "@@", "@", "char", "nchar", "varchar",
                     "select", "insert", "update", "delete", "drop", "alter", "create", 
                     "shutdown", "exec", "xp_"]
    data_lower = data.lower()
    return any(pattern in data_lower for pattern in sqli_patterns)
