document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("agregarClienteForm");
    form.addEventListener("submit", function(e) {
        e.preventDefault();

        const formData = new FormData(form);

        fetch("/clientes/agregar/", {   
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (!data.error) {
                const tbody = document.getElementById("clientesBody");
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>
                        ${data.estado === "Activo" 
                            ? '<span class="badge bg-success">Activo</span>' 
                            : '<span class="badge bg-danger">Inactivo</span>'
                        }
                    </td>
                    <td>${data.nombre}</td>
                    <td>${data.dui}</td>
                    <td>${data.nit}</td>
                    <td>${data.telefono}</td>
                    <td>${data.celular}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary">
                            <i class="bi bi-eye"></i> Ver más
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
                form.reset();
                var modal = bootstrap.Modal.getInstance(document.getElementById('agregarClienteModal'));
                modal.hide();
            }
        })
        .catch(error => console.error("Error:", error));
    });

    // Función para obtener la cookie CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
