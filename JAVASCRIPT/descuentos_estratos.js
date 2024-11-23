// --------------------------------------
// DESCUENTOS POR ESTRATO
// Introducción
// Este script solicita al usuario la cantidad de familias, el estrato de cada familia
// y el costo de tres servicios (agua, luz, gas), para calcular el descuento 
// correspondiente según el estrato.
// --------------------------------------

// Importar el módulo 'readline' para manejar la entrada de datos en la terminal
const readline = require('readline');

// Crear una interfaz para leer datos de la terminal
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// --------------------------------------
// Variables globales
// --------------------------------------
const servicios = ["Agua", "Luz", "Gas"];  // Lista de servicios públicos
let valoresFamilias = [];  // Arreglo para almacenar los datos de cada familia
let familias = 0;  // Variable para la cantidad de familias

// --------------------------------------
// Función para pedir la cantidad de familias
// --------------------------------------
function preguntarCantidadFamilias() {
  rl.question('Ingrese la cantidad de familias: ', (input) => {
    // Convertir la entrada a un número entero
    familias = parseInt(input);

    // Validar que la entrada sea un número válido
    if (isNaN(familias) || familias <= 0) {
      console.log('❌ Por favor, ingrese un número válido para la cantidad de familias.');
      preguntarCantidadFamilias();  // Volver a preguntar si la entrada no es válida
    } else {
      // Iniciar la solicitud de datos para cada familia
      preguntarDatosFamilia(0);
    }
  });
}

// --------------------------------------
// Función para pedir los datos de cada familia
// --------------------------------------
function preguntarDatosFamilia(index) {
  // Verificar si quedan familias por procesar
  if (index < familias) {
    rl.question(`Ingrese el estrato de la familia ${index + 1}: `, (estratoInput) => {
      // Convertir la entrada a un número entero
      const estrato = parseInt(estratoInput);

      // Validar que el estrato sea válido
      if (isNaN(estrato) || estrato <= 0) {
        console.log('❌ Por favor, ingrese un estrato válido.');
        preguntarDatosFamilia(index);  // Volver a preguntar si el estrato no es válido
      } else {
        // Crear un objeto para la familia actual
        let familia = { estrato, servicios: {} };

        // Iniciar la solicitud de valores para cada servicio de la familia
        preguntarValorServicio(familia, 0, index);
      }
    });
  } else {
    // Mostrar los resultados después de procesar todas las familias
    mostrarResultados();
  }
}

// --------------------------------------
// Función para pedir los valores de los servicios
// --------------------------------------
function preguntarValorServicio(familia, servicioIndex, indexFamilia) {
  // Verificar si quedan servicios por procesar
  if (servicioIndex < servicios.length) {
    const servicio = servicios[servicioIndex];  // Obtener el nombre del servicio actual
    rl.question(`Ingrese el valor del servicio de ${servicio} para la familia ${indexFamilia + 1}: `, (valorInput) => {
      // Convertir la entrada a un número flotante
      const valor = parseFloat(valorInput);

      // Validar que el valor del servicio sea válido
      if (isNaN(valor) || valor < 0) {
        console.log('❌ Por favor, ingrese un valor válido.');
        preguntarValorServicio(familia, servicioIndex, indexFamilia);  // Volver a preguntar si el valor no es válido
      } else {
        // Calcular el descuento basado en el estrato
        let descuento = 0;
        if (familia.estrato == 1) descuento = 0.20;  // 20% de descuento para estrato 1
        else if (familia.estrato == 2) descuento = 0.15;  // 15% de descuento para estrato 2
        else descuento = 0.09;  // 9% de descuento para estratos 3 o más

        // Calcular el valor del servicio con descuento
        familia.servicios[servicio] = valor - (valor * descuento);

        // Pasar al siguiente servicio
        preguntarValorServicio(familia, servicioIndex + 1, indexFamilia);
      }
    });
  } else {
    // Agregar la familia al arreglo de valores después de procesar todos los servicios
    valoresFamilias.push(familia);

    // Pasar a la siguiente familia
    preguntarDatosFamilia(indexFamilia + 1);
  }
}

// --------------------------------------
// Función para mostrar los resultados finales
// --------------------------------------
function mostrarResultados() {
  console.log('\n--- Resultados Finales ---');

  // Iterar sobre cada familia para mostrar los valores de los servicios con descuento
  valoresFamilias.forEach((familia, index) => {
    console.log(`\nFamilia ${index + 1} (Estrato ${familia.estrato}):`);

    // Iterar sobre cada servicio para mostrar el valor con descuento
    servicios.forEach(servicio => {
      console.log(`   ${servicio}: $${familia.servicios[servicio].toFixed(2)}`);
    });
  });

  rl.close();  // Cerrar la interfaz de 'readline'
}

// --------------------------------------
// Iniciar el programa
// --------------------------------------
preguntarCantidadFamilias();  // Llamar a la función inicial para empezar el flujo