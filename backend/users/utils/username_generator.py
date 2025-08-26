# users/utils.py
def generate_username(first_name: str, last_name: str) -> str:
    """Generate a lowercase username in the format firstname.lastname."""
    return f"{first_name.strip().lower()}.{last_name.strip().lower()}"
