# 🛡️ Análisis de Logs del WAF (Web Application Firewall)

---

## **1. Ataque de Inyección SQL (SQLi)**

### **Descripción del Ataque**
Se simuló un ataque de inyección SQL enviando el payload `'OR 1=1--` en el parámetro `user` de la URL.

### **Comando Utilizado**
`curl "https://tu-dominio.pages.dev/?user=admin' OR 1=1--"`

### **Resultados del WAF**
- **Fecha y Hora del Evento:** [Ingresa la fecha y hora exacta del evento en el panel de Cloudflare]
- **Dirección IP del Atacante:** [Ingresa tu dirección IP que se muestra en el log]
- **Acción Tomada por el WAF:** `Block`
- **Regla Activada:** `[Nombre de la regla personalizada que creaste]`
- **Detalles del Evento:** La petición fue bloqueada antes de llegar a la aplicación. El WAF detectó el patrón `'OR 1=1--` que coincide con la regla personalizada de SQLi.
- **Evidencia (Captura de pantalla):** [Inserta una captura de pantalla del evento en Cloudflare Analytics]

---

## **2. Ataque de Cross-Site Scripting (XSS)**

### **Descripción del Ataque**
Se simuló un ataque de XSS enviando un script (`<script>alert('XSS')</script>`) en el cuerpo del formulario de contacto.

### **Comando Utilizado**
`curl -X POST -d "message=<script>alert('XSS')</script>" "https://tu-dominio.pages.dev/submit"`

### **Resultados del WAF**
- **Fecha y Hora del Evento:** [Ingresa la fecha y hora exacta del evento en el panel de Cloudflare]
- **Dirección IP del Atacante:** [Ingresa tu dirección IP que se muestra en el log]
- **Acción Tomada por el WAF:** `Block`
- **Regla Activada:** `[Regla de Cloudflare que se activó, por lo general es una de las reglas gestionadas por defecto]`
- **Detalles del Evento:** La petición fue detenida en el borde de la red de Cloudflare. El WAF identificó la etiqueta `<script>` en el cuerpo de la petición como un patrón de ataque XSS.
- **Evidencia (Captura de pantalla):** [Inserta una captura de pantalla del evento en Cloudflare Analytics]