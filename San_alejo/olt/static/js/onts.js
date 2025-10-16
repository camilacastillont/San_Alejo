document.addEventListener("DOMContentLoaded", function() {
    const formOnt = document.getElementById("agregarOntForm");

    formOnt.addEventListener("submit", function(e) {
        e.preventDefault();

        const data = new FormData(formOnt);
        const puertoId = document.getElementById("puerto_select").value;

        fetch(`/olt/tarjetas/puerto/${puertoId}/ont/agregar/`, {
            method: "POST",
            body: data,
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        })
        .then(res => res.json())
        .then(ont => {
            if (ont.error) {
                alert(ont.error);
                return;
            }

            // Insertar la ONT en la tabla
            const tbody = document.getElementById("ontsBody");
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${ont.fsp || ''}</td>
                <td>${ont.ont_id}</td>
                <td>${ont.service_port}</td>
                <td>${ont.nombre}</td>
                <td>${ont.sn}</td>
                <td>${ont.control_flag}</td>
                <td>${ont.run_state}</td>
                <td>${ont.config_state || ''}</td>
                <td>${ont.match_state}</td>
                <td>
                    <button class="btn btn-sm btn-primary">Editar</button>
                    <button class="btn btn-sm btn-danger">Eliminar</button>
                </td>
            `;

            tbody.appendChild(row);

            // Limpiar formulario y cerrar modal
            formOnt.reset();
            bootstrap.Modal.getInstance(document.getElementById('agregarOntModal')).hide();
        })
        .catch(err => console.error("Error al agregar ONT:", err));
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
