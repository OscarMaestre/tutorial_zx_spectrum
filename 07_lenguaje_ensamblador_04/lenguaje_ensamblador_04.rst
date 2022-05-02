Lenguaje Ensamblador del Z80 (IV)
================================================================================

La pila y las llamadas a subrutinas
--------------------------------------------------------------------------------




La pila del Spectrum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



Este capítulo se centra en una de las estructuras más importantes del microprocesador Z80: la pila (o Stack en inglés).

La pila es una porción de memoria donde se pueden almacenar valores de 16 bits, apilados uno a continuación del siguiente.

Su nombre viene del hecho que los datos se almacenan unos “encima” de los otros, como, por ejemplo, en una pila de platos.

Cuando almacenamos un nuevo plato en una pila, lo dejamos en la parte superior de la misma, sobre el plato anterior. Cuando queremos coger un plato, cogemos el plato de arriba, el situado en la parte superior de la pila.

Es lo que se conoce como una estructura de datos “tipo LIFO” (“Last In, First Out”): el último que entró es el primero que sale. En nuestro ejemplo de los platos, efectivamente cuando retiramos un plato extraemos el que está arriba del todo, por lo que el primero en salir (First Out) es el último que habíamos dejado (Last In).

En una pila de ordenador (como en nuestra pila de datos) sólo podemos trabajar con el dato que está arriba del todo de la pila: no podemos extraer uno de los platos intermedios. Sólo podemos apilar un dato nuevo y desapilar el dato apilado arriba del todo de la pila.

La pila del Spectrum no es de platos sino de valores numéricos de 16 bits. Introducimos valores y sacamos valores mediante 2 instrucciones concretas: PUSH <valor> y POP <valor>, donde normalmente <valor> será un registro (metemos en la pila el valor que contiene un registro de 16 bits, o bien leemos de la pila un valor y lo asignamos a un registro de 16 bits).

Por ejemplo, podemos guardar el valor que contiene un registro en la pila si tenemos que hacer operaciones con ese registro para así luego recuperarlo tras realizar una determinada tarea:


.. code-block:: tasm

    LD BC, 1000
    PUSH BC         ; Guardamos el contenido de BC en la pila

    LD BC, 2000
    (...)           ; Operamos con BC 

    LD HL, 0
    ADD HL, BC      ; y ya podemos guardar el resultado de la operación
                    ; (recordemos que no existe "LD HL, BC", de modo que
                    ; lo almacenamos como HL = 0+BC

    POP BC          ; Hemos terminado de trabajar con BC, ahora
                    ; recuperamos el valor que tenia BC (1000).

La instrucción “PUSH BC” introduce en memoria, en lo alto de la pila, el valor contenido en BC (1000), que recuperamos posteriormente con el “POP BC”.

La realidad es que el Spectrum no tiene una zona de memoria especial o aislada de la RAM dedicada a la pila. En su lugar se utiliza la misma RAM del Spectrum (0-65535).

El Z80 tiene un registro conocido como SP (Stack Pointer), o puntero de pila, que es un registro de 16 bits que contiene una dirección de memoria. Esa dirección de memoria es “la cabeza de la pila”: apunta al próximo lugar donde almacenaremos un dato.

La peculiaridad de la pila del Spectrum es que crece hacia abajo, en lugar de hacia arriba. Veamos un ejemplo práctico: 



.. figure:: pila_z80.png
   :scale: 50%
   :align: center
   :alt: Como crece y decrece la pila del Spectrum

   Como crece y decrece la pila del Spectrum


Veámoslo con un ejemplo:

Supongamos que SP (puntero de pila) apunta a 65535 (la última posición de la memoria) y que tenemos los siguientes valores en BC y DE:

.. code-block:: tasm

    LD BC, $00FF
    LD DE, $AABB
    LD SP, 65535     ; Puntero de pila al final de la memoria

Si ahora hacemos:

.. code-block:: tasm

    PUSH BC          ; Apilamos el registro BC

Lo que estaremos haciendo es::

    SP   = SP - 2 = 65533
    (SP) =   BC   = $00FF

Con lo que el contenido de la memoria sería::
        

           Celdilla    Contenido
           -----------------------
           65534         $FF
    SP ->  65533         $00

Si a continuación hacemos otro PUSH:

.. code-block:: tasm

    PUSH DE          ; Apilamos el registro DE

Lo que estaremos haciendo es::

    SP   = SP - 2 = 65531
    (SP) =   DE   = $AABB

Con lo que el contenido de las celdillas de memoria sería::

            Celdilla    Contenido
            -----------------------
            65534         $FF
            65533         $00
            65532         $AA
    SP ->   65531         $BB

Si ahora hacemos un POP:

.. code-block:: tasm

    POP DE

Lo que hacemos es::

    DE =   (SP) = $AABB
    SP = SP + 2 = 65533

Y la memoria queda, de nuevo, como::
        
           Celdilla    Contenido
           -----------------------
           65534         $FF
    SP ->  65533         $00

Como podemos ver, PUSH apila valores, haciendo decrecer el valor de SP, mientras que POP recupera valores, haciendo crecer (en 2 bytes, 16 bits) el valor de SP.


PUSH y POP

Así pues, podemos hacer PUSH y POP de los siguientes registros:

    PUSH: AF, BC, DE, HL, IX, IY
    POP : AF, BC, DE, HL, IX, IY

Lo que hacen PUSH y POP, tal y como funciona la pila, es:

 PUSH xx :
   SP   = SP-2
   (SP) = xx
   
 POP xx :
   xx   = (SP)
   SP   = SP+2

Nótese cómo la pila se decrementa ANTES de poner los datos en ella, y se incrementa DESPUES de sacar datos de la misma. Esto mantiene siempre SP apuntando al TOS (Top Of Stack).

                        Flags 
   Instrucción       |S Z H P N C|
 ----------------------------------
 POP xx              |- - - - - -|
 PUSH xx             |- - - - - -|

Nótese que también podemos apilar y desapilar AF. De hecho, es una forma de manipular los bits del registro F (hacer PUSH BC con un valor determinado, por ejemplo, y hacer un POP AF).


Utilidad de la pila del Spectrum
--------------------------------------------------------------------------------


La pila resulta muy útil para gran cantidad de tareas en programas en ensamblador. Veamos algunos ejemplos:


* Intercambiar valores de registros mediante PUSH y POP. Por ejemplo, para intercambiar el valor de BC y de DE:

.. code-block:: tasm

    PUSH BC       ; Apilamos BC
    PUSH DE       ; Apilamos DE
    POP BC        ; Desapilamos BC 
                ; ahora BC=(valor apilado en PUSH DE)
    POP DE        ; Desapilamos DE
                ; ahora DE=(valor apilado en PUSH BC)


* Para manipular el registro F: La instrucción POP AF es la principal forma de manipular el registro F directamente (haciendo PUSH de otro registro y POP de AF).

* Almacenaje de datos mientras ejecutamos porciones de código: Supongamos que tenemos un registro cuyo valor queremos mantener, pero que tenemos que ejecutar una porción de código que lo modifica. Gracias a la pila podemos hacer lo siguiente:

.. code-block:: tasm

    PUSH BC       ; Guardamos el valor de BC
    
    (código)      ; Hacemos operaciones
    
    POP BC        ; Recuperamos el valor que teníamos en BC

Esto incluye, por ejemplo, el almacenaje del valor de BC en los bucles cuando necesitamos operador con B, C o BC:

.. code-block:: tasm

        LD A, 0
        LD B, 100
    bucle:
        PUSH BC         ; Guardamos BC
        LD B, 1
        ADD A, B
        POP BC          ; Recuperamos BC
        DJNZ bucle  

En este sentido, también podremos anidar 2 o más bucles que usen el registro B o BC con PUSH y POPs entre ellos. Supongamos un bucle BASIC del tipo:

.. code-block:: basic
        
    FOR I=0 TO 20:
        FOR J=0 TO 100:
            CODIGO
        NEXT J
    NEXT I

En ensamblador podríamos hacer:

.. code-block:: tasm

        LD B, 20                ; repetimos bucle externo 20 veces
    
    bucle_externo:
        PUSH BC                 ; Nos guardamos el valor de BC
        LD B, 100               ; Iteraciones del bucle interno
    bucle_interno:
        (... código ...)
        DJNZ bucle_interno      ; FOR J=0 TO 100
        POP BC                  ; Recuperamos el valor de B
    
        DJNZ bucle_externo      ; FOR I=0 TO 20

Hay que tener en cuenta que PUSH y POP implican escribir en memoria (en la dirección apuntada por SP), por que siempre serán más lentas que guardarse el valor actual de B en otro registro:


.. code-block:: tasm

        LD B, 20                ; repetimos bucle externo 20 veces
    
    bucle_externo:
        LD D, B                 ; Nos guardamos el valor de B
    
        LD B, 100               ; Iteraciones del bucle interno
    bucle_interno:
        (... código ...)        ; En este codigo no podemos usar D
        DJNZ bucle_interno      ; FOR J=0 TO 100
    
        LD B, D                 ; Recuperamos el valor de B
        DJNZ bucle_externo      ; FOR I=0 TO 20

No obstante, en múltiples casos nos quedaremos sin registros libres donde guardar datos, por lo que la pila es una gran opción. No hay que obsesionarse con no usar la pila porque implique escribir en memoria. A menos que estemos hablando de una rutina muy muy crítica, que se ejecute muchas veces por cada fotograma de nuestro juego, PUSH y POP serán las mejores opciones para preservar valores, con un coste de 11 t-estados para el PUSH y 10 t-estados para el POP de los registros de propósito general y de 15 y 14 t-estados cuando trabajamos con IX e IY.


* Almacenaje de datos de entrada y salida en subrutinas: Podemos pasar parámetros a nuestras rutinas apilándolos en el stack, de forma que nada más entrar en la rutina leamos de la pila esos parámetros.

* Extendiendo un poco más el punto anterior, cuando realicemos funciones en ensamblador embebidas dentro de otros lenguajes (por ejemplo, dentro de programas en C con Z88DK), podremos recoger dentro de nuestro bloque en ensamblador los parámetros pasados con llamadas de funciones C.

* Como veremos en el próximo apartado, la pila es la clave de las subrutinas (CALL/RET) en el Spectrum (equivalente al GOSUB/RETURN de BASIC).


Recordad también que tenéis instrucciones de intercambio (EX) que permiten manipular el contenido de la pila. Hablamos de:

.. code-block:: tasm

    EX (SP), HL
    EX (SP), IX
    EX (SP), IY

