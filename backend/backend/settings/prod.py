from .base import *
import dj_database_url


DEBUG = False
ALLOWED_HOSTS = ["vendor-nexus.onrender.com"]


DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# # Security hardening
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# ========================
# SECURITY HEADERS
# ========================

# Force HTTPS for all cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Make cookies inaccessible to JavaScript
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Prevent MIME type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# Prevent the site from being embedded in iframes (anti clickjacking)
# Instead of X-Frame-Options (deprecated), use CSP:
CSP_DEFAULT_SRC = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)  # blocks embedding entirely

# Enable strict HTTPS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ========================
# CACHE / PERFORMANCE
# ========================


# Additional security
SECURE_BROWSER_XSS_FILTER = True

CORS_ALLOWED_ORIGINS = [
    "https://vendor-nexus.netlify.app/",
]