document.addEventListener('DOMContentLoaded', () => {
    let users = []; // Almacena los usuarios cargados
    const securityLog = document.getElementById('security-log');
    const attackNotifications = document.getElementById('attack-notifications');

    // Función para agregar entradas al log de seguridad
    function logSecurityEvent(message, type = 'info') {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${type}`;
        logEntry.innerHTML = `[${timestamp}] ${message}`;
        securityLog.insertBefore(logEntry, securityLog.firstChild);
    }

    // Función para mostrar notificación de ataque
    function showAttackNotification(message, isBlocked = true) {
        const notification = document.createElement('div');
        notification.className = isBlocked ? 'waf-block' : 'attack-alert';
        notification.innerHTML = `
            <strong>${isBlocked ? '🛡️ Ataque Bloqueado' : '⚠️ Intento de Ataque'}</strong><br>
            ${message}
        `;
        attackNotifications.insertBefore(notification, attackNotifications.firstChild);
        setTimeout(() => notification.remove(), 5000); // Desaparece después de 5 segundos
    }

    // Función para cargar y mostrar los datos de los usuarios
    function loadUsers() {
        logSecurityEvent('🔄 Cargando datos de usuarios...');
        fetch('data.json')
            .then(response => response.json())
            .then(data => {
                users = data.users;
                displayUsers(users);
                logSecurityEvent('✅ Datos de usuarios cargados exitosamente');
            })
            .catch(error => {
                console.error('Error al cargar los datos:', error);
                const userListDiv = document.getElementById('user-list');
                userListDiv.innerHTML = '<p>No se pudieron cargar los datos de los usuarios.</p>';
                logSecurityEvent('❌ Error al cargar datos de usuarios', 'error');
            });
    }

    // Función para mostrar usuarios filtrados
    function displayUsers(usersToShow) {
        const userListDiv = document.getElementById('user-list');
        userListDiv.innerHTML = usersToShow.length ? '<h4>Usuarios encontrados:</h4>' : '<p>No se encontraron usuarios.</p>';
        
        usersToShow.forEach(user => {
            const userItem = document.createElement('div');
            userItem.className = 'user-item';
            userItem.innerHTML = `
                <strong>ID:</strong> ${user.id} |
                <strong>Usuario:</strong> ${user.username} |
                <strong>Estado:</strong> ${user.status}
            `;
            userListDiv.appendChild(userItem);
        });
    }

    // Maneja la búsqueda de usuarios (objetivo SQLi)
    const searchForm = document.getElementById('searchForm');
    const searchResponse = document.getElementById('search-response');
    
    searchForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const searchQuery = document.getElementById('searchQuery').value;
        
        // Detectar posibles patrones de SQLi
        const sqlInjectionPatterns = [
            "'", "--", "OR", "AND", "UNION", "SELECT", "DROP", "DELETE", "UPDATE"
        ];
        
        const containsSQLi = sqlInjectionPatterns.some(pattern => 
            searchQuery.toUpperCase().includes(pattern.toUpperCase())
        );
        
        if (containsSQLi) {
            showAttackNotification(`Intento de SQLi detectado en la búsqueda: "${searchQuery}"`, true);
            searchResponse.innerHTML = `
                <div class="waf-block">
                    🛡️ WAF ha bloqueado un posible ataque SQLi<br>
                    Query maliciosa detectada
                </div>`;
            logSecurityEvent(`⚠️ Intento de SQLi bloqueado: ${searchQuery}`, 'warning');
            return;
        }

        // Simular búsqueda normal
        const filteredUsers = users.filter(user => 
            user.username.toLowerCase().includes(searchQuery.toLowerCase())
        );
        displayUsers(filteredUsers);
        logSecurityEvent(`🔍 Búsqueda realizada: "${searchQuery}"`);
    });

    // Maneja el envío del formulario de contacto (objetivo XSS)
    const contactForm = document.getElementById('contactForm');
    const formResponseDiv = document.getElementById('form-response');
    const commentsSection = document.getElementById('comments-section');
    
    contactForm.addEventListener('submit', (event) => {
        event.preventDefault();
        
        const username = document.getElementById('username').value;
        const message = document.getElementById('message').value;
        
        // Detectar posibles patrones de XSS
        const xssPatterns = [
            "<script", "javascript:", "onerror=", "onload=", "<img", "<iframe"
        ];
        
        const containsXSS = xssPatterns.some(pattern => 
            message.toLowerCase().includes(pattern.toLowerCase()) ||
            username.toLowerCase().includes(pattern.toLowerCase())
        );
        
        if (containsXSS) {
            showAttackNotification(`Intento de XSS detectado en el mensaje`, true);
            formResponseDiv.innerHTML = `
                <div class="waf-block">
                    🛡️ WAF ha bloqueado un posible ataque XSS<br>
                    Contenido malicioso detectado
                </div>`;
            logSecurityEvent(`⚠️ Intento de XSS bloqueado en mensaje de: ${username}`, 'warning');
            return;
        }

        // Procesar mensaje normal
        const commentDiv = document.createElement('div');
        commentDiv.className = 'user-item';
        commentDiv.innerHTML = `
            <strong>${username}</strong> dice:<br>
            ${message}
        `;
        commentsSection.insertBefore(commentDiv, commentsSection.firstChild);
        
        formResponseDiv.innerHTML = `
            <div class="waf-block">
                ✅ Mensaje enviado exitosamente
            </div>`;
        
        logSecurityEvent(`✉️ Nuevo comentario de: ${username}`);
        
        // Limpiar el formulario
        contactForm.reset();
    });

    // Inicializar la página
    loadUsers();

});