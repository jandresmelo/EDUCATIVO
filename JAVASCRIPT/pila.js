/**
 * --------------------------------------
 * Introducción a la Pila en JavaScript
 * 
 * Una pila (stack) es una estructura de datos que sigue el principio 
 * LIFO (Last In, First Out), es decir, el último elemento que entra 
 * es el primero en salir.
 * 
 * Este código implementa una pila básica en JavaScript con operaciones como:
 * 1. Insertar (push)
 * 2. Eliminar (pop)
 * 3. Buscar un elemento
 * 4. Actualizar un elemento
 * 5. Mostrar todos los elementos de la pila
 * --------------------------------------
 */

class Pila {
    /**
     * Constructor de la clase Pila
     * @param {number} maximo - Capacidad máxima de la pila
     */
    constructor(maximo) {
        this.tope = -1;  // Índice de la parte superior de la pila, inicia en -1 (vacía)
        this.maximo = maximo;  // Capacidad máxima de la pila
        this.vectorElementos = new Array(maximo);  // Arreglo para almacenar los elementos
    }

    /**
     * Método para insertar (push) un elemento en la pila
     * @param {number} elemento - Elemento a insertar en la pila
     */
    push(elemento) {
        if (this.tope < this.maximo - 1) {  // Verifica si hay espacio en la pila
            this.tope++;  // Incrementa el tope
            this.vectorElementos[this.tope] = elemento;  // Inserta el elemento en la pila
            console.log(`Elemento ${elemento} insertado en la pila.`);
        } else {
            console.log('⚠️ La pila está llena. No se pueden insertar más elementos.');
        }
    }

    /**
     * Método para eliminar (pop) el elemento superior de la pila
     * @returns {number|null} - Elemento eliminado o null si la pila está vacía
     */
    pop() {
        if (this.tope >= 0) {  // Verifica si la pila no está vacía
            const elementoEliminado = this.vectorElementos[this.tope];  // Guarda el elemento eliminado
            this.tope--;  // Decrementa el tope
            console.log(`Elemento ${elementoEliminado} eliminado de la pila.`);
            return elementoEliminado;  // Retorna el elemento eliminado
        } else {
            console.log('⚠️ La pila está vacía. No se puede eliminar ningún elemento.');
            return null;
        }
    }

    /**
     * Método para buscar un elemento en la pila
     * @param {number} elemento - Elemento a buscar en la pila
     * @returns {number} - Índice del elemento encontrado o -1 si no se encuentra
     */
    buscar(elemento) {
        for (let i = 0; i <= this.tope; i++) {
            if (this.vectorElementos[i] === elemento) {  // Compara cada elemento
                console.log(`Elemento ${elemento} encontrado en la posición ${i}.`);
                return i;  // Retorna el índice si se encuentra el elemento
            }
        }
        console.log(`Elemento ${elemento} no encontrado en la pila.`);
        return -1;  // Retorna -1 si no se encuentra el elemento
    }

    /**
     * Método para actualizar un elemento en la pila
     * @param {number} posicion - Posición a actualizar
     * @param {number} nuevoValor - Nuevo valor a asignar
     */
    actualizar(posicion, nuevoValor) {
        if (posicion >= 0 && posicion <= this.tope) {  // Verifica si la posición es válida
            this.vectorElementos[posicion] = nuevoValor;  // Actualiza el valor en la posición
            console.log(`Elemento en la posición ${posicion} actualizado a ${nuevoValor}.`);
        } else {
            console.log('⚠️ Posición no válida para actualizar.');
        }
    }

    /**
     * Método para mostrar todos los elementos de la pila
     */
    imprimir() {
        if (this.tope >= 0) {  // Verifica si la pila no está vacía
            console.log('\n--- Elementos en la pila ---');
            for (let i = 0; i <= this.tope; i++) {
                console.log(`Posición ${i}: ${this.vectorElementos[i]}`);  // Imprime cada elemento
            }
        } else {
            console.log('⚠️ La pila está vacía. No hay elementos para mostrar.');
        }
    }
}

// --------------------------------------
// Ejemplo de uso de la Pila en JavaScript
// --------------------------------------

const pila = new Pila(5);  // Crear una pila con capacidad máxima de 5

// Insertar elementos en la pila
pila.push(10);  // Inserta 10 en la pila
pila.push(20);  // Inserta 20 en la pila
pila.push(30);  // Inserta 30 en la pila
pila.imprimir();  // Mostrar los elementos actuales de la pila

// Eliminar el elemento superior de la pila
pila.pop();  // Elimina el elemento en la parte superior
pila.imprimir();  // Mostrar los elementos después de eliminar

// Buscar un elemento en la pila
pila.buscar(20);  // Buscar el elemento 20 en la pila

// Actualizar un elemento en la pila
pila.actualizar(0, 50);  // Actualiza el elemento en la posición 0 a 50
pila.imprimir();  // Mostrar los elementos después de la actualización