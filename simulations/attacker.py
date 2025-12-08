import requests #pip install requests
import json
import time
from datetime import datetime

# Reemplaza esta URL con la que te dio Cloudflare Pages
URL_APLICACION = "https://www.proyredes.art"

def enviar_log_ataque(mensaje, tipo="info"):
    """Envía un log de ataque a la página web."""
    try:
        datos = {
            "tipo": tipo,
            "mensaje": mensaje,
            "timestamp": datetime.now().strftime("%I:%M:%S %p"),
            "origen": "Atacante"
        }
        # Nota: Si el WAF es muy estricto, podría bloquear también este log.
        requests.post(f"{URL_APLICACION}/log", json=datos, timeout=2)
    except:
        # Si falla el envío, continuamos con el ataque silenciosamente
        pass

def analizar_respuesta_waf(respuesta):
    """
    Analiza críticamente la respuesta para distinguir entre:
    1. Bloqueo duro (WAF Block)
    2. Desafío Interactivo (Managed Challenge / CAPTCHA)
    3. Acceso permitido (Fallo de seguridad)
    """
    html_content = respuesta.text
    status = respuesta.status_code
    headers = respuesta.headers

    # Firmas típicas de un Managed Challenge de Cloudflare
    firmas_challenge = [
        "Just a moment",
        "Enable JavaScript",
        "challenge-platform",
        "verifying you are human",
        "turnstile"
    ]
    
    es_challenge = any(firma in html_content for firma in firmas_challenge)

    print(f"\n    Resultados del Análisis:")
    print(f"    Código de respuesta: {status}")
    print(f"    Headers relevantes: cf-ray={headers.get('cf-ray', 'N/A')}")

    if es_challenge:
        mensaje = "🤖 ✅ ÉXITO: Cloudflare lanzó un MANAGED CHALLENGE (CAPTCHA/JS)."
        detalle = "    El script se quedó atascado en la pantalla de verificación. Un humano vería el CAPTCHA."
        print(f"\n    {mensaje}")
        print(detalle)
        return "challenge", headers.get('cf-ray')
    
    elif status == 403:
        mensaje = "🛡️ ✅ ÉXITO: WAF bloqueó el ataque (Hard Block)."
        print(f"\n    {mensaje}")
        return "block", headers.get('cf-ray')
        
    elif status == 200:
        mensaje = "❌ FALLO: El ataque pasó exitosamente (Status 200)."
        print(f"\n    {mensaje}")
        print("    Contenido parcial:", html_content[:100].replace('\n', ' '))
        return "pass", None
    
    else:
        print(f"\n    ⚠️ Estado inesperado: {status}")
        return "unknown", None

def simular_ataque_sqli():
    print("🚀 Iniciando simulación de ataques SQL Injection (SQLi)...")
    payloads = [
        "' OR '1'='1",
        "' UNION SELECT * FROM users--",
        "'; DROP TABLE users--"
    ]
    
    for i, payload in enumerate(payloads, 1):
        print(f"\n📌 Prueba SQLi #{i} - Payload: {payload}")
        enviar_log_ataque(f"⚠️ Test SQLi #{i}", "warning")
        
        url = f"{URL_APLICACION}/?search={payload}"
        
        try:
            # User-Agent malicioso típico para forzar reglas
            headers = {"User-Agent": payload} 
            respuesta = requests.get(url, headers=headers)
            analizar_respuesta_waf(respuesta)
            time.sleep(0.5)
        except Exception as e:
            print(f"    ❌ Error: {e}")

def simular_ataque_xss():
    print("\n\n🚀 Iniciando simulación de ataques XSS...")
    payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert(1)>"
    ]
    
    for i, payload in enumerate(payloads, 1):
        print(f"\n📌 Prueba XSS #{i} - Payload: {payload}")
        enviar_log_ataque(f"⚠️ Test XSS #{i}", "warning")
        
        # Prueba GET
        try:
            print("    [GET Request]")
            headers = {"Referer": payload} # Cloudflare suele mirar Referer o URI
            respuesta = requests.get(f"{URL_APLICACION}/?input={payload}", headers=headers)
            analizar_respuesta_waf(respuesta)
        except Exception as e:
            print(f"    ❌ Error: {e}")

def simular_ataque_bot():
    """
    Simula una 'Botnet' con 6 identidades diferentes 
    para probar la consistencia del Managed Challenge (CAPTCHA).
    """
    print("\n\n🤖 Iniciando simulación de BOTNET (6 Intentos)...")
    print("ℹ️  Objetivo: Verificar que Cloudflare detiene múltiples intentos automatizados.")
    
    # La "llave" para activar tu regla de Cloudflare
    parametro_trigger = "simular_bot=1" 
    url = f"{URL_APLICACION}/?{parametro_trigger}"
    
    # Lista ampliada a 6 "identidades" para simular diferentes herramientas de ataque
    user_agents_bots = [
        "python-requests/script-malicioso-v1",       # 1. Script básico
        "Mozilla/5.0 (compatible; EvilBot/1.0)",     # 2. Bot autodeclarado
        "curl/7.64.1 (headless-scraper)",            # 3. Herramienta de consola
        "Go-http-client/1.1 (bot-network)",          # 4. Bot escrito en Go
        "Apache-HttpClient/4.5.13 (Java/1.8)",       # 5. Bot basado en Java
        "Wget/1.21.1 (linux-gnu)"                    # 6. Descargador clásico
    ]

    for i, agente in enumerate(user_agents_bots, 1):
        print(f"\n📌 Intento de Bot #{i} de 6")
        print(f"    Identidad simulada: {agente}")
        
        try:
            headers = {
                'User-Agent': agente,
                'Accept': 'text/html,application/xhtml+xml'
            }
            
            # Pequeña pausa para asegurar que el log se vea ordenado
            if i > 1: time.sleep(1.5)
            
            respuesta = requests.get(url, headers=headers)
            resultado, ray_id = analizar_respuesta_waf(respuesta)
            
            if resultado == "challenge":
                 enviar_log_ataque(f"✅ Bot #{i} detenido por Captcha. RayID: {ray_id}", "success")
            elif resultado == "block":
                 enviar_log_ataque(f"✅ Bot #{i} bloqueado totalmente. RayID: {ray_id}", "success")
            else:
                 enviar_log_ataque(f"❌ Bot #{i} logró entrar sin desafío.", "danger")

        except requests.exceptions.RequestException as e:
            print(f"    ❌ Error de conexión: {e}")

if __name__ == "__main__":
    print("\n🔒 AUDITORÍA DE SEGURIDAD - CLOUDFLARE EDGE 🔒")
    print("=" * 60)
    print(f"Objetivo: {URL_APLICACION}")
    print("=" * 60)
    
    input("\nPresiona Enter para iniciar la batería de pruebas...")
    
    simular_ataque_sqli()
    simular_ataque_xss()
    simular_ataque_bot() # <-- Nueva llamada a la función
    
    print("\n" + "=" * 60)
    print("🏁 Auditoría finalizada.")