window.onload = function() {
    console.log('Window onload event triggered');
    // Primero, obtén los datos básicos de los usuarios
    fetch('http://44.207.140.112:5000/users')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log('Usuarios obtenidos:', data);
        const table = document.getElementById('usersTable').getElementsByTagName('tbody')[0];
        
        // Procesar cada usuario
        data.forEach(user => {
            console.log('Procesando usuario:', user);
            // Crear una fila para cada usuario
            let row = table.insertRow();
            
            // Inicializar la fila con los datos básicos del usuario
            row.innerHTML = `
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.age}</td>
                <td id="money-${user.id}">Cargando...</td> <!-- Placeholder para el dinero -->
                <td id="debt-${user.id}">Cargando...</td> <!-- Placeholder para la deuda -->
                <td>
                    <button class="update">Actualizar</button>
                    <button class="delete">Eliminar</button>
                </td>
            `;

            // Hacer un fetch adicional para obtener el dinero del usuario
            fetch(`http://44.207.140.112:8001/bank/${user.id}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(bankData => {
                console.log('Dinero obtenido para el usuario:', user.id, bankData);
                const moneyElement = document.getElementById(`money-${user.id}`);
                if (bankData.length > 0) {
                    moneyElement.textContent = bankData[0].money;
                } else {
                    moneyElement.textContent = "No disponible";
                }
            })
            .catch(error => {
                console.error(`Error al cargar el dinero del usuario ${user.id}:`, error);
                const moneyElement = document.getElementById(`money-${user.id}`);
                moneyElement.textContent = "No tiene dinero";
            });

            // Hacer un fetch adicional para obtener la deuda del usuario
            fetch(`http://44.207.140.112:8005/debts/${user.id}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(debtData => {
                console.log('Deuda obtenida para el usuario:', user.id, debtData);
                const debtElement = document.getElementById(`debt-${user.id}`);
                if (debtData.length > 0) {
                    debtElement.textContent = debtData[0].debt;
                } else {
                    debtElement.textContent = "No disponible";
                }
            })
            .catch(error => {
                console.error(`Error al cargar la deuda del usuario ${user.id}:`, error);
                const debtElement = document.getElementById(`debt-${user.id}`);
                debtElement.textContent = "No tiene deuda";
            });
        });
    })
    .catch(error => console.error('Error al cargar los usuarios:', error));

    document.getElementById('usersTable').addEventListener('click', function(e) {
        if (e.target.classList.contains('update')) {
            const id = e.target.closest('tr').querySelector('td:first-child').textContent;
            console.log('Actualizar usuario con ID:', id);
            // Lógica para actualizar usuario
        } else if (e.target.classList.contains('delete')) {
            const id = e.target.closest('tr').querySelector('td:first-child').textContent;
            console.log('Eliminar usuario con ID:', id);
            // Lógica para eliminar usuarioo
        }
    });

    document.getElementById('addUser').addEventListener('click', function() {
        alert('Aquí podrías abrir un modal o redirigir a una página para agregar un nuevo usuario.');
        // Lógica para abrir un modal de formulario o redirigir a una página de agregar usuario
    });
};



