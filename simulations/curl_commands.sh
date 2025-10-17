#!/bin/bash

# Este script contiene los comandos para simular ataques a tu aplicación web
# en Cloudflare Pages y verificar la protección del WAF.

# Reemplaza esta variable con la URL de tu sitio en Cloudflare Pages
# Ejemplo: https://proyecto-firewall.pages.dev
DOMAIN="https://www.proyredes.art"

echo "=========================================="
echo "Iniciando simulaciones de ataque con cURL"
echo "=========================================="

# --- Simulación de Inyección SQL (SQLi) ---
# Este comando intenta inyectar código malicioso en la URL para
# acceder a datos protegidos de la base de datos.

echo -e "\n---> Probando Inyección SQL (SQLi) con payload 'OR 1=1--"
curl -s -o /dev/null -w "%{http_code}\n" "${DOMAIN}/?user=admin' OR 1=1--"

# Si la regla del WAF está configurada correctamente, la respuesta debería ser 403 (Forbidden).
echo "Verifica el código de respuesta. Un 403 significa que el ataque fue bloqueado."

# --- Simulación de Cross-Site Scripting (XSS) ---
# Este comando intenta inyectar un script en el cuerpo de una petición POST.

echo -e "\n---> Probando Cross-Site Scripting (XSS) con payload <script>alert('XSS')</script>"
curl -s -o /dev/null -w "%{http_code}\n" -X POST -d "message=<script>alert('XSS')</script>" "${DOMAIN}/submit"

# La regla predefinida del WAF de Cloudflare debería bloquear este ataque,
# resultando también en un código de respuesta 403.
echo "Verifica el código de respuesta. Un 403 significa que el ataque fue bloqueado."

echo -e "\n=========================================="
echo "Simulaciones de ataque finalizadas."
echo "Revisa el panel de Cloudflare para ver los eventos de seguridad."
echo "=========================================="