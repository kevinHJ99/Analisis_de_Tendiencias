# Activar el middleware de proxy
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 1,
    "scrapy_rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
    "scrapy_rotating_proxies.middlewares.BanDetectionMiddleware": 620,
}

# Lista de proxies (usa proxies confiables)
# ROTATING_PROXY_LIST = [
#     "http://usuario:contraseña@proxy1.com:port",
#     "http://usuario:contraseña@proxy2.com:port",
#     "http://proxy3.com:port",
#     "http://proxy4.com:port",
# ]

# Alternativa: Cargar proxies desde un archivo
ROTATING_PROXY_LIST_PATH = "proxies.txt"

# Configuración adicional
CONCURRENT_REQUESTS = 5  # Número de solicitudes simultáneas
DOWNLOAD_DELAY = 2  # Evita bloqueos con pausas entre requests
