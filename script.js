document.addEventListener('DOMContentLoaded', () => {

    // Función para cargar y mostrar los datos de los usuarios
    function loadUsers() {
        fetch('data.json')
            .then(response => response.json())
            .then(data => {
                const userListDiv = document.getElementById('user-list');
                userListDiv.innerHTML = '<h4>Datos cargados exitosamente:</h4>';
                
                // Muestra cada usuario en la página
                data.users.forEach(user => {
                    const userItem = document.createElement('div');
                    userItem.className = 'user-item';
                    userItem.innerHTML = `
                        <strong>ID:</strong> ${user.id} |
                        <strong>Usuario:</strong> ${user.username} |
                        <strong>Estado:</strong> ${user.status}
                    `;
                    userListDiv.appendChild(userItem);
                });
            })
            .catch(error => {
                console.error('Error al cargar los datos:', error);
                const userListDiv = document.getElementById('user-list');
                userListDiv.innerHTML = '<p>No se pudieron cargar los datos de los usuarios.</p>';
            });
    }

    // Maneja el envío del formulario de contacto
    const contactForm = document.getElementById('contactForm');
    const formResponseDiv = document.getElementById('form-response');
    
    contactForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Evita que el formulario se envíe de forma tradicional
        
        const message = document.getElementById('message').value;
        formResponseDiv.textContent = `Mensaje recibido: "${message}".`;
        formResponseDiv.style.color = 'green';

        // En un escenario real, esta petición iría al servidor
        // y sería el objetivo del WAF para ataques como XSS.
    });

    // Llama a la función para cargar los datos al iniciar la página
    loadUsers();

});