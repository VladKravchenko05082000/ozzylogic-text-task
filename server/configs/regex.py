import re

PASSWORD_RE = re.compile(r"^(?=.*[A-Za-z])(?=.*\d).{8,20}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
DATE_ONLY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")