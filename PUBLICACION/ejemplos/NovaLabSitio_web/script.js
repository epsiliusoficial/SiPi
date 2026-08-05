document.getElementById("boton-principal").addEventListener("click", function () {
  const contador = (script_js_contador = (window.script_js_contador || 0) + 1);
  window.script_js_contador = contador;
  document.getElementById("mensaje").textContent = "Presionaste el boton " + contador + " veces (esto es JavaScript real).";
});
