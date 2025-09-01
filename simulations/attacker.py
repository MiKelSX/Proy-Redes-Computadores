import requests #pip install requests
import json
import time

# Reemplaza esta URL con la que te dio Cloudflare Pages
URL_APLICACION = "https://tu-dominio.pages.dev"

def simular_ataque_sqli():
    """Simula un ataque de inyección SQL."""
    print("🚀 Simulación de ataque de Inyección SQL (SQLi)...")
    
    # Payload común de SQLi
    payload = "' OR 1=1--"
    
    # La petición maliciosa se envía en la URL
    peticion_sqli = f"{URL_APLICACION}/?search={payload}"
    
    try:
        respuesta = requests.get(peticion_sqli)
        print("Estatus de la respuesta:", respuesta.status_code)
        print("Contenido de la respuesta (primeras 200 caracteres):")
        print(respuesta.text[:200])
        
        if respuesta.status_code == 403:
            print("\n✅ El WAF de Cloudflare ha bloqueado el ataque (código de error 403 Forbidden).")
        else:
            print("\n❌ El ataque no fue bloqueado. Revisa tus reglas en Cloudflare.")
    except requests.exceptions.RequestException as e:
        print(f"Ocurrió un error: {e}")

def simular_ataque_xss():
    """Simula un ataque de Cross-Site Scripting (XSS)."""
    print("\n\n🚀 Simulación de ataque de Cross-Site Scripting (XSS)...")
    
    # Payload de XSS que intentaría inyectar un script
    payload_xss = "<script>alert('Ataque XSS exitoso')</script>"
    
    # Se envía el payload en el cuerpo de una petición POST, como si fuera un formulario
    datos_formulario = {
        "mensaje": payload_xss
    }
    
    # Cloudflare WAF también revisa el cuerpo de las peticiones POST
    try:
        respuesta = requests.post(f"{URL_APLICACION}/submit", data=datos_formulario)
        print("Estatus de la respuesta:", respuesta.status_code)
        print("Contenido de la respuesta (primeras 200 caracteres):")
        print(respuesta.text[:200])
        
        if respuesta.status_code == 403:
            print("\n✅ El WAF de Cloudflare ha bloqueado el ataque (código de error 403 Forbidden).")
        else:
            print("\n❌ El ataque no fue bloqueado. Revisa tus reglas en Cloudflare.")
    except requests.exceptions.RequestException as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    print("Iniciando el script de ataque de seguridad para tu proyecto en Cloudflare.")
    print("-" * 50)
    
    # Ejecutar la simulación de SQLi
    simular_ataque_sqli()
    
    print("\n" + "=" * 50 + "\n")
    time.sleep(2) # Espera 2 segundos antes del siguiente ataque
    
    # Ejecutar la simulación de XSS
    simular_ataque_xss()