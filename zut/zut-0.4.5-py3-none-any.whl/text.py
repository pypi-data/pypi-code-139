from __future__ import annotations
import re, unicodedata

# if tuple, second element is the original Django's slugify result
SLUGEN_EXAMPLES = {
    "Hello world":                  "hello-world",
    "  \"Privilège\" : élevé!-:) ": "privilege-eleve",
    "--__ _-ADMIN_-_SYS_#_":        ("admin-sys", "admin_-_sys"),
    "Pas d'problème":               ("pas-d-probleme", "pas-dprobleme"),
    "L ' horloge":                  "l-horloge",
    "Main (detail)":                "main-detail",
    "__-__":                        "",
    "---":                          "",
    "-":                            "",
    "#":                            "",
    "":                             "",
    None:                           ("", "none"),
}

def slugen(value, separator='-') -> str:
    """ 
    Generate a slug.

    Simplier alternative to `django.utils.text.slugify`.
    See `SLUGEN_EXAMPLES` for differences.
    """
    if value is None:
        return ""
    
    # Remove accents and other diacritic/non-ascii characters
    value = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")

    # Lowercase the string
    value = value.lower()

    # Replace everything that is not a letter or digit by hyphens
    value = re.sub(r"[^a-z0-9]", "-", value)

    # Trim leading, trailing, and consecutive hyphens
    return re.sub(r"-+", separator, value).strip(separator)
