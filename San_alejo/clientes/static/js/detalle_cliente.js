document.addEventListener("DOMContentLoaded", () => {
  const btnGuardar = document.getElementById("guardarCambios");
  const form = document.getElementById("formActualizarCliente");
  const alerta = document.getElementById("alerta");

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie("csrftoken");
  const clienteId = window.location.pathname.split("/").filter(Boolean).pop();

  btnGuardar.addEventListener("click", async () => {
    const formData = new FormData(form);
    try {
      const response = await fetch(`/clientes/actualizar/${clienteId}/`, {
        method: "POST",
        headers: { "X-CSRFToken": csrftoken },
        body: formData,
      });

      const data = await response.json();
      alerta.classList.remove("d-none", "alert-danger", "alert-success");

      if (data.success) {
        alerta.classList.add("alert-success");
        alerta.textContent = data.message;
      } else {
        alerta.classList.add("alert-danger");
        alerta.textContent = "Error al guardar los cambios.";
      }
    } catch (error) {
      alerta.classList.remove("d-none");
      alerta.classList.add("alert-danger");
      alerta.textContent = "Error al conectar con el servidor.";
      console.error(error);
    }
  });
});
