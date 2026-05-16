import re

PASSWORD_RE = re.compile(r"^(?=.*[A-Za-z])(?=.*\d).{8,20}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")