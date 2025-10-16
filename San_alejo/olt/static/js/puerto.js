document.addEventListener("DOMContentLoaded", function() {
    const formPuerto = document.getElementById("agregarPuertoForm");

    formPuerto.addEventListener("submit", function(e) {
        e.preventDefault();

        const data = new FormData(formPuerto);
        const tarjetaId = document.getElementById("tarjetaId").value;

        fetch(`/olt/tarjeta/${tarjetaId}/puerto/agregar/`, {
            method: "POST",
            body: data,
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
        .then(res => res.json())
        .then(puerto => {
            if(puerto.error){
                alert(puerto.error);
                return;
            }

            // Insertar el nuevo puerto en la tabla
            const tbody = document.getElementById("puertosBody");
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${puerto.id}</td>
                <td>${puerto.port}</td>
                <td>${puerto.tipo}</td>
                <td>${puerto.min_distance}</td>
                <td>${puerto.max_distance}</td>
                <td><span class="badge ${puerto.status === 'Offline' ? 'bg-danger' : 'bg-success'}">${puerto.status}</span></td>
                <td>
                    <button class="btn btn-sm btn-primary">Editar</button>
                    <button class="btn btn-sm btn-danger">Eliminar</button>
                </td>
            `;
            tbody.appendChild(row);

            // Limpiar formulario y cerrar modal
            formPuerto.reset();
            bootstrap.Modal.getInstance(document.getElementById('agregarPuertoModal')).hide();
        })
        .catch(err => console.error("Error al agregar puerto:", err));
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            document.cookie.split(";").forEach(cookie => {
                const [key, value] = cookie.trim().split("=");
                if (key === name) cookieValue = value;
            });
        }
        return cookieValue;
    }
});
