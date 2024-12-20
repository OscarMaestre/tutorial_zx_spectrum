Lenguaje Ensamblador del Z80 (III)
================================================================================



Instrucciones condicionales
--------------------------------------------------------------------------------



Una vez hemos visto la mayoría de instrucciones aritméticas y lógicas, es el momento de utilizarlas como condicionales para realizar cambios en el flujo lineal de nuestro programa. En esta entrega aprenderemos a usar etiquetas y saltos mediante instrucciones condicionales (CP, JR + condición, JP + condición, etc.), lo que nos permitirá implementar en ensamblador las típicas instrucciones IF/THEN/ELSE y los GOTO de BASIC.


Las etiquetas en los programas ASM
--------------------------------------------------------------------------------

Las etiquetas son unas útiles directivas de los ensambladores que nos permitirán hacer referencia a posiciones concretas de memoria por medio de nombres, en lugar de tener que utilizar valores numéricos.

Veamos un ejemplo de etiqueta en un programa ensamblador: 

.. code-block:: tasm

        ORG 50000

        NOP
        LD B, 10
    bucle:
        LD A, 20
        NOP
        ...
        JP bucle
        RET



Este es el código binario que genera el listado anterior al ser ensamblado::

    00 06 0a 3e 14 00 (...) c3 53 c3 c9

Concretamente: 

+-----------+----------+------------------+
| DIRECCIÓN | OPCODE   | INSTRUCCION      |
+===========+==========+==================+
| 50000     | 00       | NOP              |
+-----------+----------+------------------+
| 50001     | 06 0a    | LD B, 10         |
+-----------+----------+------------------+
| 50003     | 3e 14    | LD A, 20         |
+-----------+----------+------------------+
| 50004     | 00       | NOP              |
+-----------+----------+------------------+
| ...       | ...      | ...              |
+-----------+----------+------------------+
|           | c3 53 c3 | JP $C353 (53000) |
+-----------+----------+------------------+
| ...+1     | c9       | RET              |
+-----------+----------+------------------+


Si mostramos las direcciones de memoria en que se ensambla cada instrucción, veremos::

    50000   NOP              ; opcode = 1 byte
    50001   LD B, 10         ; opcode = 2 bytes
    50003   LD A, 20         ; opcode = 2 bytes
    50005   NOP              ; opcode = 1 byte
    50005   más código
    50006   más código
    50020   JP bucle
    50023   RET

¿Dónde está en ese listado de instrucciones nuestra etiqueta "bucle"? Sencillo: no está. No es ninguna instrucción, sino, para el ensamblador, una referencia a la celdilla de memoria 50003, donde está la instrucción que sigue a la etiqueta.

En nuestro ejemplo anterior, le decimos al programa ensamblador mediante ORG 50000 que nuestro código, una vez ensamblado, debe quedar situado a partir de la dirección 50000, con lo cual cuando calcule las direcciones de las etiquetas deberá hacerlo en relación a esta dirección de origen. Así, en nuestro ejemplo anterior la instrucción NOP, que se ensambla con el opcode $00, será "pokeada" (por nuestro cargador BASIC) en la dirección 50000. La instrucción LD B, 10, cuyo opcode tiene 2 bytes, será "pokeada" en 50001 y 50002, y así con todas las instrucciones del programa.

Cuando el ensamblador se encuentra la etiqueta "bucle:" después del "LD B, 10", ¿cómo la ensambla? Supuestamente le corresponde la posición 50003, pero recordemos que esto no es una instrucción, sino una etiqueta: no tiene ningún significado para el microprocesador, sólo para el programa ensamblador. Por eso, cuando el ensamblador encuentra la etiqueta "bucle:", asocia internamente esta etiqueta (el texto "bucle") a la dirección 50003, que es la dirección donde hemos puesto la etiqueta.

Si la etiqueta fuera una instrucción, se ensamblaría en la dirección 50003, pero como no lo es, el programa ensamblador simplemente la agrega a una tabla interna de referencias, donde lo que anota es:


* La etiqueta "bucle" apunta a la dirección 50003


Lo que realmente ensamblará en la dirección 50003 (y en la 50004) es la instrucción siguiente: "LD A, 20".

Pero, entonces, ¿para qué nos sirve la etiqueta? Sencillo: para poder hacer referencia en cualquier momento a esa posición de memoria (del programa, en este caso), mediante una cadena fácil de recordar en lugar de mediante un número. Es más sencillo recordar "bucle" que recordar "50003", y si nuestro programa es largo y tenemos muchos saltos, funciones o variables, acabaremos utilizando decenas y centenares de números para saltos, con lo que el programa sería inmanejable.

El siguiente programa es equivalente al anterior, pero sin usar etiquetas:

    
    ORG 50000
        NOP
        LD B, 10
        LD A, 20
        NOP
        continúa...
        JP 50003
        RET

En este caso, "JP 50003" no permite distinguir rápidamente a qué instrucción vamos a saltar, mientras que la etiqueta "bucle" que utilizamos en el anterior ejemplo marcaba de forma indiscutible el destino del salto.

Las etiquetas son muy útiles no sólo por motivos de legibilidad del código. Imaginemos que una vez acabado nuestro programa sin etiquetas (utilizando sólo direcciones numéricas), con muchos saltos (JP, CALL, JR, DJNZ...) a diferentes partes del mismo, tenemos que modificarlo para corregir alguna parte del mismo. Al añadir o quitar instrucciones del programa, estamos variando las posiciones donde se ensambla todo el programa. Si por ejemplo, añadiéramos un NOP extra al principio del mismo, ya no habría que saltar a 50003 sino a 50004:


.. code-block:: tasm

    ORG 50000

    NOP
    NOP        ; Un NOP extra
    LD B, 10
    LD A, 20
    NOP
    ;(...)
    JP 50004   ; La dirección de salto cambia
    RET

Para que nuestro programa funcione, tendríamos que cambiar TODAS las direcciones numéricas de salto del programa, a mano (recalculandolas todas). Las etiquetas evitan esto, ya que es el programa ensamblador quien, en tiempo de ensamblado, cuando está convirtiendo el programa a código objeto, cambia todas las referencias a la etiqueta por el valor numérico correcto (por la posición donde aparece la etiqueta). Un "JP bucle" siempre saltaría a la dirección correcta (la de la posición de la etiqueta) aunque cambiemos la cantidad de instrucciones del programa.

Como veremos posteriormente, la instrucción JP realiza un salto de ejecución de código a una posición de memoria dada. Literalmente, un JP XX hace el registro PC = XX, de forma que alteramos el orden de ejecución del programa. Las etiquetas nos permiten establecer posiciones donde saltar en nuestro programa para utilizarlas luego fácilmente: 

.. code-block:: tasm
    
    ORG 50000
    
    ; Al salir de esta rutina, A=tecla pulsada
    RutinaLeerTeclado:
    ;(instrucciones)    ; Aquí código
    RET
    
    ; Saltar (JP) a esta rutina con:
    ;  HL = Sprite a dibujar
    ;  DE = Direccion en pantalla donde dibujar
    RutinaDibujarSprite:
    ;(...)
    bucle1:
        ;(instrucciones)
    bucle2:
        ;(instrucciones)
    pintar:
        ;(instrucciones)
        JP bucle1
        ;resto omitido
    salir:
    RET
        ;etc...

Así, podremos especificar múltiples etiquetas para hacer referencia a todas las posiciones que necesitemos dentro de nuestro programa.

Lo que nos tiene que quedar claro de este apartado son dos conceptos: cuando el ensamblador encuentra la definición de una etiqueta, guarda en una tabla interna la dirección de ensamblado de la siguiente instrucción a dicha etiqueta. Después, cada vez que hay una aparición de esa etiqueta en el código, sustituye la etiqueta por dicha dirección de memoria. Además, podemos utilizar la etiqueta incluso aunque la definamos después (más adelante) del código, ya que el ensamblador hace varias pasadas en la compilación: no es necesario primero definir la etiqueta y después hacer referencia a ella, podemos hacerlo también a la inversa.

Es decir, es válido tanto:

.. code-block:: tasm
    
    etiqueta:
        ;;; (más código)
        JP etiqueta

Como:

.. code-block:: tasm

        JP etiqueta
        ;;; (más código)
    etiqueta:


Como vamos a ver, también podemos utilizar etiquetas para referenciar a bloques de datos, cadenas de texto, gráficos y en general cualquier tipo de dato en crudo que queramos insertar dentro de nuestro programa.



Definir datos y referenciarlos con etiquetas
--------------------------------------------------------------------------------




Podemos insertar en cualquier posición de la memoria y de nuestro programa datos en formato numérico o de texto con directivas como **DB (DEFB), DW (DEFW) o DS (DEFS)**, y hacer referencia a ellos mediante etiquetas.

Por ejemplo: 

.. code-block:: tasm

 ; Principio del programa
 ORG 50000
 
   ; Primero vamos a copiar los datos a la videomemoria.
   LD HL, datos
   LD DE, 16384
   LD BC, 10
   LDIR
 
   ; Ahora vamos a sumar 1 a cada carácter:
   LD B, 27
  bucle:
   LD HL, texto
   LD A, (HL)
   INC A
   LD (HL), A
 
   DJNZ bucle
   RET
   datos DB 0, $FF, $FF, 0, $FF, 12, 0, 0, 0, 10, 255
   texto DB "Esto es una cadena de texto"
 
   ; Fin del programa
   END



.. figure:: db.png
   :scale: 120%
   :align: center
   :alt: Resultado de RANDOMIZE USR 50000 en nuestro programa

   Resultado de RANDOMIZE USR 50000 en nuestro programa


Como puede verse, con DB hemos "insertado" datos directamente dentro de nuestro programa. Estos datos se cargarán en memoria (pokeados) también como parte del programa, y podremos acceder a ellos posteriormente. Los datos, en nuestro programa, están situados en la memoria, justo después de las instrucciones ensambladas (tras el último RET). Podemos verlo si ensamblamos el programa::

    $ pasmo --bin db.asm db.bin

    $ hexdump -C db.bin
    00000000  21 66 c3 11 00 40 01 0a  00 ed b0 06 1b 21 71 c3  |!f...@.......!q.|
    00000010  7e 3c 77 10 f8 c9 00 ff  ff 00 ff 0c 00 00 00 0a  |~<w.............|
    00000020  ff 45 73 74 6f 20 65 73  20 75 6e 61 20 63 61 64  |.Esto es una cad|
    00000030  65 6e 61 20 64 65 20 74  65 78 74 6f              |ena de texto|
    0000003c

Si os fijáis, podemos ver el RET (201, o $C9) justo antes del bloque de datos FF, FF, 0, FF. Concretamente, la etiqueta "datos" en el programa hará referencia (al pokear el programa a partir de 50000), a la posición de memoria 50022, que contendrá el 00 inicial de nuestros datos DB.

Cuando en el programa hacemos "LD HL, datos", el ensamblador transforma esa instrucción en realidad en "LD HL, 50022" (fijaos en el principio del programa: 21 66 C3, que corresponde a LD HL, C366, que es 50022). Gracias a esto podemos manipular los datos (que están en memoria) y leerlos y cambiarlos, utilizando un "nombre" como referencia a la celdilla de memoria de inicio de los mismos.

Lo mismo ocurre con el texto que se ha definido entre dobles comillas. A partir de la dirección definida por "texto" se colocan todos los bytes que forman la cadena "Esto es una cadena de texto". Cada byte en memoria es una letra de la cadena, en formato ASCII (La "E" es $45, la "s" es $73", etc.).

Con DB (o DEFB, que es un equivalente por compatibilidad con otros ensambladores) podremos definir:


* Cadenas de texto (todos los mensajes de texto de nuestros programas/juegos).
* Datos numéricos con los que trabajar (bytes, words, caracteres...).
* Tablas precalculadas para optimizar. Por ejemplo, podemos tener un listado como el siguiente::

     numeros_primos  DB  1, 3, 5, 7, 11, 13, (etc...)


* Variables en memoria para trabajar en nuestro programa:: 

    vidas  DB   3
    x      DB   0
    y      DB   0
    ancho  DB  16
    alto   DB  16
    (...)
    
    LD A, (vidas)
    (...)
    muerte:
    DEC A
    LD (vidas), A

* Datos gráficos de nuestros sprites (creados con utilidades como SevenuP o ZXPaintBrush, por ejemplo)::

    Enemigo:
        DB 12, 13, 25, 123, 210 (etc...)

Ahora bien, es muy importante tener clara una consideración: los datos que introducimos con DB (o DW, o cualquier otra directiva de inclusión) no se ensamblan, pero se insertan dentro del código resultante tal cual. Y el Z80 no puede distinguir un 201 introducido con DB de un opcode 201 (RET), con lo cual tenemos que asegurarnos de que dicho código no se ejecute, como en el siguiente programa:


.. code-block:: tasm

    ORG 50000
    
    ; Cuidado, al situar los datos aquí, cuando saltemos a 50000
    ; con RANDOMIZE USR 50000, ejecutaremos estos datos como si
    ; fueran opcodes.
    datos DB 00, 201, 100, 12, 255, 11
    
    LD B, A
    ;(más instrucciones)
    RET
 
Lo correcto sería:
 
.. code-block:: tasm
    
    ORG 50000

    ; Ahora el salto a 50000 ejecutará el LD B, A, no los
    ; datos que habíamos introducido antes.
    LD B, A
    ;(más instrucciones)
    RET

    ; Aquí nunca serán ejecutados, el RET está antes.
    datos DB 00, 201, 100, 12, 255, 11

Los microprocesadores como el Z80 no saben distinguir entre datos e instrucciones, y es por eso que tenemos que tener cuidado de no ejecutar datos como si fueran códigos de instrucción del Z80. De hecho, si hacemos un RANDOMIZE USR XX (siendo XX cualquier valor de la memoria fuera de la ROM), lo más probable es que ejecutemos datos como si fueran instrucciones y el Spectrum se cuelgue, ya que los datos no son parte de un programa, y la ejecución resultante de interpretar esos datos no tendría ningún sentido.


Saltos absolutos incondicionales: JP
--------------------------------------------------------------------------------



Ya sabemos definir etiquetas en nuestros programas y referenciarlas. Ahora la pregunta es: ¿para qué sirven estas etiquetas? Aparte de referencias para usarlas como variables o datos, su principal uso será saltar a ellas con las instrucciones de salto.

Para empezar vamos a ver 2 instrucciones de salto incondicionales, es decir, cuando lleguemos a una de esas 2 instrucciones, se modificará el registro PC para cambiar la ejecución del programa. De esta forma podremos realizar bucles, saltos a rutinas o funciones, etc.

Empecemos con JP (abreviatura de JumP):

.. code-block:: tasm

    ; Ejemplo de un programa con un bucle infinito
        ORG 50000
    
        XOR A               ; A = 0
    bucle:
        INC A               ; A = A + 1
        LD (16384), A       ; Escribir valor de A en (16384)
        JP bucle   
    
        RET                 ; Esto nunca se ejecutará
    
        END 50000


¿Qué hace el ejemplo anterior? Ensamblémoslo con ``pasmo –tapbas bucle.asm bucle.tap``  y carguémoslo en BASIC.

Nada más entrar en 50000, se ejecuta un "INC A". Después se hace un "LD (16384), A", es decir, escribimos en la celdilla (16384) de la memoria el valor que contiene A. Esta celdilla se corresponde con los primeros 8 píxeles de la pantalla, con lo cual estaremos cambiando el contenido de la misma.

Tras esta escritura, encontramos un "JP bucle", que lo que hace es cambiar el valor de PC y hacerlo, de nuevo, PC=50000. El código se volverá a repetir, y de nuevo al llegar a JP volveremos a saltar a la dirección definida por la etiqueta "bucle". Es un bucle infinito, realizado gracias a este salto incondicional (podemos reiniciar el Spectrum para retomar el control). Estaremos repitiendo una y otra vez la misma porción de código, que cambia el contenido de los 8 primeros píxeles de pantalla poniendo en ellos el valor de A (que varía desde 0 a 255 continuadamente).

Utilizaremos pues JP para cambiar el rumbo del programa y cambiar PC para ejecutar otras porciones de código (anteriores o posteriores a la posición actual) del mismo. JP realiza pues lo que se conoce como "SALTO INCONDICIONAL ABSOLUTO", es decir, saltar a una posición absoluta de memoria (una celdilla de 0 a 65535), mediante la asignación de dicho valor al registro PC.

Existen 3 maneras de usar JP: 

* JP NN: Saltar a la dirección NN. Literalmente: PC = NN
* JP (HL):  Saltar a la dirección contenida en el registro HL (ojo, no a la dirección apuntada por el registro HL, sino directamente a su valor). Literalmente: PC = HL
* JP (registro_indice): Saltar a la dirección contenida en IX o IY. Literalmente: PC = IX o PC = IY


Saltos relativos incondicionales: JR
--------------------------------------------------------------------------------


Además de JP, tenemos otra instrucción para realizar saltos incondicionales: JR. JR trabaja exactamente igual que JP: realiza un salto (cambiando el valor del registro PC), pero lo hace de forma diferente.

JR son las siglas de "Jump Relative", y es que esta instrucción en lugar de realizar un salto absoluto (a una posición de memoria 0-65535), lo hace de forma relativa, es decir, a una posición de memoria alrededor de la posición actual (una vez decodificada la instrucción JR).

El argumento de JR no es pues un valor numérico de 16 bits (0-65535) sino un valor de 8 bits en complemento a dos que nos permite saltar desde la posición actual (referenciada en el ensamblador como "$") hasta 127 bytes hacia adelante y 127 bytes hacia atrás:

Ejemplos de instrucciones JR: 

.. code-block:: tasm

    JR $+25      ; Saltar adelante 25 bytes: PC = PC+25
    JR $-100     ; Saltar atrás 100 bytes:   PC = PC-100

Nosotros, gracias a las etiquetas, podemos olvidarnos de calcular posiciones y hacer referencia de una forma más sencilla a posiciones en nuestro programa:

Veamos el mismo ejemplo anterior de JP, con JR: 

.. code-block:: tasm

        ; Ejemplo de un programa con un bucle infinito
        ORG 50000
    
    bucle:
        INC A
        LD (16384), A
        JR bucle   
    
        RET ; Esto nunca se ejecutará


Como puede verse, el ejemplo es exactamente igual que en el caso anterior. No tenemos que utilizar el carácter $ (posición actual de ensamblado) porque al hacer uso de etiquetas es el ensamblador quien se encarga de traducir la etiqueta a un desplazamiento de 8 bits y ensamblarlo.

¿Qué diferencia tiene JP con JR? Pues bien: para empezar en lugar de ocupar 3 bytes (JP + la dirección de 16 bits), ocupa sólo 2 (JR + el desplazamiento de 8 bits) con lo cual se decodifica y ejecuta más rápido.

Además, como la dirección del salto no es absoluta, sino relativa, y de 8 bits en complemento a dos, no podemos saltar a cualquier punto del programa, sino que sólo podremos saltar a código que esté cerca de la línea actual: como máximo 127 bytes por encima o por debajo de la posición actual en memoria.

Si tratamos de ensamblar un salto a una etiqueta que está más allá del alcance de un salto relativo, obtendremos un error como el siguiente::

    ERROR: Relative jump out of range

En ese caso, tendremos que cambiar la instrucción "JR etiqueta" por un "JP etiqueta", de forma que el ensamblador utilice un salto absoluto que le permita llegar a la posición de memoria que queremos saltar y que está más alejada de que la capacidad de salto de JR.

¿Cuál es la utilidad o ventaja de los saltos relativos aparte de ocupar 2 bytes en lugar de 3? Pues que los saltos realizados en rutinas que usen JR y no JP son todos relativos a la posición actual, con lo cual la rutina es REUBICABLE. Es decir, si cambiamos nuestra rutina de 50000 a 60000 (por ejemplo), funcionará, porque los saltos son relativos a "$". En una rutina programada con JP, si la pokeamos en 60000 en lugar de en 50000, cuando hagamos saltos (JP 50003, por ejemplo), saltaremos a lugares donde no está el código (ahora está en 60003) y el programa no hará lo que esperamos. En resumen: JR permite programar rutinas reubicables y JP no.

(Nota: se dice que una rutina es reubicable cuando estando programada a partir de una determinada dirección de memoria, podemos copiar la rutina a otra dirección y sus saltos funcionarán correctamente por no ser absolutos).

¿Recordáis en los cursos y rutinas de Microhobby cuando se decía "Esta rutina es reubicable"? Pues quería decir exactamente eso, que podías copiar la rutina en cualquier lugar de la memoria y llamarla, dado que el autor de la misma había utilizado sólo saltos relativos y no absolutos, por lo que daría igual la posición de memoria en que la POKEaramos.

En nuestro caso, al usar un programa ensamblador en lugar de simplemente disponer de las rutinas en código máquina (ya ensambladas) que nos mostraba microhobby, no se nos plantearán esos problemas, dado que nosotros podemos usar etiquetas y copiar cualquier porción del código a dónde queramos de nuestro programa. Aquellas rutinas etiquetadas como "reubicables" o "no reubicables" estaban ensambladas manualmente y utilizaban direcciones de memoria numéricas o saltos absolutos.

Nuestro ensamblador (Pasmo, z80asm, etc) nos permite utilizar etiquetas, que serán reemplazadas por sus direcciones de memoria durante el proceso de ensamblado. Nosotros podemos modificar las posibles de nuestras rutinas en el código, y dejar que el ensamblador las "reubique" por nosotros, ya que al ensamblará cambiará todas las referencias a las etiquetas que usamos.

Esta facilidad de trabajo contrasta con las dificultades que tenían los programadores de la época que no disponían de ensambladores profesionales. Imaginad la cantidad de usuarios que ensamblaban sus programas a mano, usando saltos relativos y absolutos (y como veremos, llamadas a subrutinas), que en lugar de sencillos nombres (JP A_mayor_que_B) utilizaban directamente direcciones en memoria.

E imaginad el trabajo que suponía mantener un listado en papel todas los direcciones de saltos, subrutinas y variables, referenciados por direcciones de memoria y no por nombres, y tener que cambiar muchos de ellos cada vez que tenían que arreglar un fallo en una subrutina y cambiaban los destinos de los saltos por crecer el código que había entre ellos.

Dejando ese tema aparte, la tabla de afectación de flags de JR es la misma que para JP: nula::
 
                            Flags 
    Instrucción       |S Z H P N C|
    ----------------------------------
    JR d              |- - - - - -|

    (Donde "d" es un desplazamiento de 8 bits)

Literalmente, JR d se traduce por PC=PC+d. 


Saltos condicionales con los flags
--------------------------------------------------------------------------------



Ya hemos visto la forma de realizar saltos incondicionales. A continuación veremos cómo realizar los saltos (ya sean absolutos con JP o relativos con JR) de acuerdo a unas determinadas condiciones.

Las instrucciones condicionales disponibles trabajan con el estado de los flags del registro F, y son:


* JP NZ, direccion : Salta si el indicador de cero (Z) está a cero (resultado no cero).
* JP Z, direccion : Salta si el indicador de cero (Z) está a uno (resultado cero).
* JP NC, direccion : Salta si el indicador de carry (C) está a cero.
* JP C, direccion : Salta si el indicador de carry (C) está a uno.
* JP PO, direccion : Salta si el indicador de paridad/desbordamiento (P/O) está a cero.
* JP PE, direccion : Salta si el indicador de paridad/desbordamiento (P/O) está a uno.
* JP P, direccion : Salta si el indicador de signo S está a cero (resultado positivo).
* JP M, direccion : Salta si el indicador de signo S está a uno (resultado negativo).
* JR NZ, relativo : Salta si el indicador de cero (Z) está a cero (resultado no cero).
* JR Z, relativo : Salta si el indicador de cero (Z) está a uno (resultado cero).
* JR NC, relativo : Salta si el indicador de carry (C) está a cero.
* JR C, relativo : Salta si el indicador de carry (C) está a uno.

Donde "dirección" es un valor absoluto 0-65535, y "relativo" es un desplazamiento de 8 bits con signo -127 a +127.

(Nota: en el listado de instrucciones, positivo o negativo se refiere a considerando el resultado de la operación anterior en complemento a dos).

Así, supongamos el siguiente programa:

.. code-block:: tasm

        JP Z, destino
        LD A, 10
    destino:
        NOP

(donde "destino" es una etiqueta definida en algún lugar de nuestro programa, aunque también habríamos podido especificar directamente una dirección como por ejemplo 50004).

Cuando el procesador lee el "JP Z, destino", lo que hace es lo siguiente:

* Si el flag Z está activado (a uno), saltamos a "destino" (con lo cual no se ejecuta el "LD A, 10"), ejecutándose el código a partir del "NOP".
* Si no está activo (a cero) no se realiza ningún salto, con lo que se ejecutaría el "LD A, 10", y seguiría después con el "NOP".

En BASIC, "JP Z, destino" sería algo como:

.. code-block:: basic

    IF FLAG_ZERO = 1 THEN GOTO destino

Y "JP NZ, destino" sería:

.. code-block:: basic

    IF FLAG_ZERO = 0 THEN GOTO destino

Con estas instrucciones podemos realizar saltos condicionales en función del estado de los flags o indicadores del registro F: podemos saltar si el resultado de una operación es cero, si no es cero, si hubo acarreo, si no lo hubo...

Y el lector se preguntará: ¿y tiene utilidad realizar saltos en función de los flags? Pues la respuesta es: bien usados, lo tiene para todo tipo de tareas:


.. code-block:: tasm

        ; Repetir 100 veces la instruccion NOP
        LD A, 100
    bucle:
        NOP
        
        DEC A          ; Decrementamos A.
                        ; Cuando A sea cero, Z se pondrá a 1
        JR NZ, bucle   ; Mientras Z=0, repetir el bucle
        LD A, 200      ; Aquí llegaremos cuando Z sea 1 (A valga 0)
        ; resto del programa

Es decir: cargamos en A el valor 100, y tras ejecutar la instrucción "NOP", hacemos un "DEC A" que decrementa su valor (a 99). Como el resultado de "DEC A" es 99 y no cero, el flag de Z (de cero) se queda a 0, (recordemos que sólo se pone a uno cuando la última operación resultó ser cero).

Y como el flag Z es cero (NON ZERO = no activado el flag zero) la instrucción "JR NZ, bucle" realiza un salto a la etiqueta "bucle". Allí se ejecuta el NOP y de nuevo el "DEC A", dejando ahora A en 98.

Tras repetirse 100 veces el proceso, llegará un momento en que A valga cero tras el "DEC A". En ese momento se activará el flag de ZERO con lo que la instrucción "JR NZ, bucle" no realizará el salto y continuará con el "LD A, 200".

Veamos otro ejemplo más gráfico: vamos a implementar en ASM una comparación de igualdad:


.. code-block:: basic

    IF A=B THEN GOTO iguales ELSE GOTO distintos

En ensamblador:


.. code-block:: tasm

   SUB B              ; A = A-B
   JR Z, iguales      ; Si Z=1 saltar a iguales 
   JR NZ, distintos   ; Si Z=0 saltar a distintos 
 
iguales:

.. code-block:: tasm

    ;;; (código)
        JR seguir
    distintos:
        ;;; (código)
        JR seguir
        
        seguir:


(Nota: se podría haber usado JP en vez de JR)

Para comparar A con B los restamos (A=A-B). Si el resultado de la resta es cero, es porque A era igual a B. Si no es cero, es que eran distintos. Y utilizando el flag de Zero con JP Z y JP NZ podemos detectar esa diferencia.

Pronto veremos más a fondo otras instrucciones de comparación, pero este ejemplo debe bastar para demostrar la importancia de los flags y de su uso en instrucciones de salto condicionales. Bien utilizadas podemos alterar el flujo del programa a voluntad. Es cierto que no es tan inmediato ni cómodo como los >, <, = y <> de BASIC, pero el resultado es el mismo, y es fácil acostumbrarse a este tipo de comparaciones mediante el estado de los flags.

Para finalizar, un detalle sobre DEC+JR: La combinación DEC B / JR NZ se puede sustituir (es más eficiente, y más sencillo) por el comando DJNZ, que literalmente significa "Decrementa B y si no es cero, salta a <direccion>".


DJNZ direccion

Equivale a decrementar B y a la dirección indicada en caso de que B no valga cero tras el decremento.

Esta instrucción se usa habitualmente en bucles (usando B como iterador del mismo) y, al igual que JP y JR, no afecta al estado de los flags::

                            Flags 
    Instrucción       |S Z H P N C|
    ----------------------------------
    |JP COND, NN       |- - - - - -|
    |JR COND, d        |- - - - - -|
    |DJNZ d            |- - - - - -|


El argumento de salto de DJNZ es de 1 byte, por lo que para saltos relativos de más de 127 bytes hacia atrás o hacia adelante (-127 a +127), DJNZ se tiene que sustituir por la siguiente combinación de instrucciones:

.. code-block:: tasm

  DEC B                      ; Decrementar B, afecta a los flags
  JP NZ, direccion           ; Salto absoluto: permite cualquier distancia


DJNZ trabaja con el registro B como contador de repeticiones, lo que implica que podemos realizar de 0 a 255 iteraciones. En caso de necesitar realizar hasta 65535 iteraciones tendremos que utilizar un registro de 16 bits como BC de la siguiente forma:

.. code-block:: tasm

   DEC BC                    ; Decrementamos BC -> no afecta a los flags
   LD A, B                   ; Cargamos B en A
   OR C                      ; Hacemos OR a de A y C (de B y C)
   JR NZ, direccion          ; Si (B OR C) no es cero, BC != 0, saltar

Instruccion de comparacion CP
--------------------------------------------------------------------------------




Comparaciones de 8 bits

Para realizar comparaciones (especialmente de igualdad, mayor que y menor que) utilizaremos la instrucción CP. Su formato es::
    
    CP origen

Donde "origen" puede ser A, F, B, C, D, E, H, L, un valor numérico de 8 bits directo, (HL), (IX+d) o (IY+d).

Al realizar una instrucción "CP origen", el microprocesador ejecuta la operación "A-origen", pero no almacena el resultado en ningún sitio. Lo que sí que hace es alterar el estado de los flags de acuerdo al resultado de la operación.

Recordemos el ejemplo de comparación anterior donde realizábamos una resta, perdiendo por tanto el valor de A:

.. code-block:: tasm

   SUB B                  ; A = A-B
   JR Z, iguales          ; Si Z=1 saltar a iguales
   JR NZ, distintos       ; Si Z=0 saltar a distintos

Gracias a CP, podemos hacer la misma operación pero sin perder el valor de A (por la resta):

   CP B                   ; Flags = estado(A-B)
   JR Z, iguales          ; Si Z=1 saltar a iguales
   JR NZ, distintos       ; Si Z=0 saltar a distintos

¿Qué nos permite esto? Aprovechando todos los flags del registro F (flag de acarreo, flag de zero, etc), realizar comparaciones como las siguientes:

.. code-block:: tasm

        ; Comparación entre A Y B (=, > y <)
        LD B, 5
        LD A, 3
        
        CP B                            ; Flags = estado(A-B)
        JP Z, A_Igual_que_B             ; IF(a-b)=0 THEN a=b
        JP NC, A_Mayor_o_igual_que_B    ; IF(a-b)>0 THEN a>=b
        JP C, A_Menor_que_B             ; IF(a-b)<0 THEN a<b
        
    A_Mayor_que_B:
        ;;; (instrucciones)
        JP fin
        
    A_Menor_que_B:
        ;;; (instrucciones)
        JP fin
        
    A_Igual_que_B:
        ;;; (instrucciones)
        
    fin:
        ;;; (continúa el programa)

Vamos a ilustrar la anterior porción de código con un ejemplo que nos permitirá, además, descubrir una forma muy singular de hacer debugging en vuestras pruebas aprendiendo ensamblador. Vamos a sacar información por pantalla de forma que podamos ver en qué parte del programa estamos. Este mismo "sistema" podéis emplearlo (hasta que veamos cómo sacar texto o gráficos concretos por pantalla) para "depurar" vuestros programas y hacer pruebas.

Consiste en escribir un valor en la memoria, justo en la zona de la pantalla, para así distinguir las partes de nuestro programa por las que pasamos. Así, escribiremos 255 (8 pixeles activos) en una línea de la parte superior de la pantalla izquierda (16960), en el centro de la misma (19056), o en la parte inferior derecha (21470):

.. code-block:: tasm

        ; Principio del programa
        ORG 50000
        
        ; Comparacion entre A Y B (=, > y <)
        LD B, 7
        LD A, 5
        
        CP B                    ; Flags = estado(A-B)
        JP Z, A_Igual_que_B     ; IF(a-b)=0 THEN a=b
        JP NC, A_Mayor_que_B    ; IF(a-b)>0 THEN a>b
        JP C, A_Menor_que_B     ; IF(a-b)<0 THEN a<b
        
    A_Mayor_que_B:
        LD A, 255
        LD (16960), A           ; 8 pixels en la parte sup-izq
        JP fin
        
    A_Menor_que_B:
        LD A, 255
        LD (19056), A           ; centro de la pantalla
        JP fin
        
    A_Igual_que_B:
        LD A, 255
        LD (21470), A           ; parte inferior derecha
        
    fin:
        JP fin                  ; bucle infinito, para que podamos ver 
                                ; el resultado de la ejecucion
        
        END 50000

Lo ensamblamos con: ``pasmo –tapbas compara.asm compara.tap``, y lo cargamos en el Spectrum o emulador. La sentencia END 50000 nos ahorra el teclear "RANDOMIZE USR 50000" ya que pasmo lo introducirá en el cargador BASIC por nosotros. Jugando con los valores de A y B del listado deberemos ver cómo cambia el lugar al que saltamos (representado por el lugar de la pantalla en que vemos dibujada nuestra pequeña línea de 8 píxeles).


Salida del programa anterior con A=5 y B=7



.. figure:: compara.png
   :scale: 80%
   :align: center
   :alt: Salida del programa anterior con A=5 y B=7

   Salida del programa anterior con A=5 y B=7



Finalmente, destacar que nada nos impide el hacer comparaciones multiples o anidadas:

.. code-block:: tasm
            
        LD B, 5
        LD A, 3
        LD C, 6
        
        CP B                  ; IF A==B
        JR Z, A_Igual_a_B     ; THEN goto A_Igual_a_B
        CP C                  ; IF A==C
        JR Z, A_Igual_a_C     ; THEN goto A_Igual_a_C
        JP Fin                ; si no, salimos
    A_Igual_a_B:
        ; (Omitido)
        JR Fin
        
    A_Igual_a_C:
        ; (Omitido)
        
    Fin:
        ;(resto del programa)

La instrucción CP afecta a todos los flags::

                            Flags 
    Instrucción       |S Z H P N C|
    ----------------------------------
    |CP s               |* * * V 1 *|

El flag "N" se pone a uno porque, aunque se ignore el resultado, la operación efectuada es una resta. 



Comparaciones de 16 bits
--------------------------------------------------------------------------------



Aunque la instrucción CP sólo permite comparar un valor de 8 bits con el valor contenido en el registro A, podemos realizar 2 comparaciones CP para verificar si un valor de 16 bits es menor, igual o mayor que otro.

Si lo que queremos comparar es un registro con otro, podemos hacerlo mediante un CP de su parte alta y su parte baja. Por ejemplo, para comparar HL con DE:

.. code-block:: tasm
            
        ;;; Comparacion 16 bits de HL y DE
        LD A, H
        CP D
        JR NZ, no_iguales
        LD A, L
        CP E
        JR NZ, no_iguales
    iguales:
        ;;; (...)
        
    no_iguales:
        ;;; (...)

Para comparar si el valor de un registro es igual a un valor numérico inmediato (introducido directamente en el código de programa), utilizaríamos el siguiente código:

.. code-block:: tasm
            
        ;;; Comparacion 16 bits de HL y VALOR_NUMERICO (inmediato)
        ;;; VALOR_NUMERICO puede ser cualquier valor de 0 a 65535
        LD A, H
        CP VALOR_NUMERICO / 256         ; Parte alta (VALOR/256)
        JR NZ, no_iguales
        LD A, L
        CP VALOR_NUMERICO % 256         ; Parte baja (Resto de VALOR/256)
        JR NZ, no_iguales
    iguales:
        ;;; (...)
        
    no_iguales:
        ;;; (...)


Consideraciones de las condiciones
--------------------------------------------------------------------------------



A la hora de utilizar instrucciones condicionales hay que tener en cuenta que no todas las instrucciones afectan a los flags. Por ejemplo, la instrucción "DEC BC" no pondrá el flag Z a uno cuando BC sea cero. Si intentamos montar un bucle mediante DEC BC + JR NZ, nunca saldremos del mismo, ya que DEC BC no afecta al flag de zero.


.. code-block:: tasm
        
        LD BC, 1000        ; BC = 1000
    bucle:
        ; (Omitido...)
    
        DEC BC             ; BC = BC-1 (pero NO ALTERA el Carry Flag)
        JR NZ, bucle       ; Nunca se pondrá a uno el ZF, siempre salta

Para evitar estas situaciones necesitamos conocer la afectación de los flags ante cada instrucción, que podéis consultar en todas las tablas que os hemos proporcionado.

Podemos realizar algo similar al ejemplo anterior aprovechándonos (de nuevo) de los flags y de los resultados de las operaciones lógicas (y sus efectos sobre el registro F). Como ya vimos al tratar la instrucción DJNZ, podemos comprobar si un registro de 16 bits vale 0 realizando un OR entre la parte alta y la parte baja del mismo. Esto sí afectará a los flags y permitirá realizar el salto condicional:

.. code-block:: tasm

        LD BC, 1000        ; BC = 1000
 
    bucle:
        ; (Omitido...)
        DEC BC             ; Decrementamos BC. No afecta a F.
        LD A, B            ; A = B
        OR C               ; A = A OR C 
                        ; Esto sí que afecta a los flags.
                        ; Si B==C y ambos son cero, el resultado
                        ; del OR será cero y el ZF se pondrá a 1.
        JR NZ, bucle       ; ahora sí que funcionará el salto si BC=0

Más detalles sobre los saltos condicionales: esta vez respecto al signo. Las condiciones P y M (JP P, JP M) nos permitirán realizar saltos según el estado del bit de signo. Resultará especialmente útil después de operaciones aritméticas.

Los saltos por Paridad/Overflow (JP PO, JP PE) permitirán realizar saltos en función de la paridad cuando la última operación realizada modifique ese bit de F según la paridad del resultado. La misma condición nos servirá para desbordamientos si la última operación que afecta a flags realizada modifica este bit con respecto a dicha condición.

¿Qué quiere decir esto? Que si, por ejemplo, realizamos una suma o resta, JP PO y JP PE responderán en función de si ha habido un desbordamiento o no y no en función de la paridad, porque las sumas y restas actualizan dicho flag según los desbordamientos, no según la paridad.


La importancia de la probabilidad de salto
--------------------------------------------------------------------------------



Ante una instrucción condicional, el microprocesador tendrá 2 opciones, según los valores que comparemos y el tipo de comparación que hagamos (si es cero, si no es cero, si es mayor o menor, etc.). Al final, sólo habrá 2 caminos posibles: saltar a una dirección de destino, o no saltar y continuar en la dirección de memoria siguiente al salto condicional.

Aunque pueda parecer una pérdida de tiempo, en rutinas críticas es muy interesante el pararse a pensar cuál puede ser el caso con más probabilidades de ejecución, ya que el tiempo empleado en la opción "CONDICION CIERTA, POR LO QUE SE PRODUCE EL SALTO" es mayor que el empleado en "CONDICION FALSA, NO SALTO Y SIGO".

Por ejemplo, ante un "JP Z, direccion", el microprocesador tardará 10 ciclos de reloj en ejecutar un salto si la condición se cumple, y sólo 1 si no se cumple (ya que entonces no tiene que realizar salto alguno).

Supongamos que tenemos una rutina crítica donde la velocidad es importante. Vamos a utilizar, como ejemplo, la siguiente rutina que devuelve 1 si el parámetro que le pasamos es mayor que 250 y devuelve 0 si es menor:

.. code-block:: tasm
            
        ; Comparar A con 250:
        ;
        ; Devuelve A = 0 si A < 250
        ;          A = 1 si A > 250
        
    Valor_Mayor_Que_250:
        
        CP 250                      ; Comparamos A con 250
        JP C, A_menor_que_250       ; Si es menor, saltamos
        LD A, 1                     ; si es mayor, devolvemos 1
        RET
        
    A_menor_que_250:
        LD A, 0
        RET

En el ejemplo anterior se produce el salto si A es menor que 250 (10 t-estados) y no se produce si A es mayor que 250 (1 t-estado).

Supongamos que llamamos a esta rutina con 1000 valores diferentes. En ese caso, existen más probabilidades de que el valor esté entre 0 y 250 a que esté entre 250 y 255, por lo que sería más óptimo que el salto que hay dentro de la rutina se haga no cuando A sea menor que 250 sino cuando A sea mayor, de forma que se produzcan menos saltos.

Lo normal es que, ante datos aleatorios, haya más probabilidad de encontrar datos del segundo caso (0-250) que del primero (250-255), simplemente por el hecho de que del primer caso hay 250 probabilides de 255, mientras que del segundo hay 5 probabilidades de 255.

En tal caso, la rutina debería organizarse de forma que la comparación realice el salto cuando encuentre un dato mayor de 250, dado que ese supuesto se dará menos veces. Si lo hicieramos a la inversa, se saltaría más veces y la rutina tardaría más en realizar el mismo trabajo.

.. code-block:: tasm
            
        ; Comparar A con 250:
        ;
        ; Devuelve A = 0 si A < 250
        ;          A = 1 si A > 250
        
    Valor_Mayor_Que_250:
        
        CP 250                      ; Comparamos A con 250
        JP NC, A_mayor_que_250      ; Si es mayor, saltamos
        LD A, 0                     ; si es menor, devolvemos 1
        RET
        
    A_mayor_que_250:
        LD A, 1
        RET

Eso hace que haya más posibilidades de no saltar que de saltar, es decir, de emplear un ciclo de procesador y no 10 para la mayoría de las ejecuciones.


Instrucciones de comparacion repetitivas
--------------------------------------------------------------------------------



Para acabar con las instrucciones de comparación vamos a ver las instrucciones de comparación repetitivas. Son parecidas a CP, pero trabajan (igual que LDI, LDIR, LDD y LDDR) con HL y BC para realizar las comparaciones con la memoria: son CPI, CPD, CPIR y CPDR.

Comencemos con CPI (ComPare and Increment):



CPI:

* Al registro A se le resta el byte contenido en la posición de memoria apuntada por HL.
* El resultado de la resta no se almacena en ningún sitio.
* Los flags resultan afectados por la comparación:
    * Si A==(HL), se pone a 1 el flag de Zero (si no es igual se pone a 0).
    * Si BC==0000, se pone a 0 el flag Parity/Overflow (a 1 en caso contrario).
* Se incrementa HL.
* Se decrementa BC.

Técnicamente (con un pequeño matiz que veremos ahora), CPI equivale a::
    
 CPI =     CP [HL]
           INC HL
           DEC BC


CPD:
Su instrucción "hermana" CPD (ComPare and Decrement) funciona de idéntica forma, pero decrementando HL::

 CPD =     CP [HL]
           DEC HL
           DEC BC

Y el pequeño matiz: así como CP [HL] afecta al indicador C de Carry, CPI y CPD, aunque realizan esa operación intermedia, no lo afectan.

Las instrucciones CPIR y CPDR son equivalentes a CPI y CPD, pero ejecutándose múltiples veces: hasta que BC sea cero o bien se encuentre en la posición de memoria apuntada por HL un valor numérico igual al que contiene el registro A. Literalmente, es una instrucción de búsqueda: buscamos hacia adelante (CPIR) o hacia atrás (CPDR), desde una posición de memoria inicial (HL), un valor (A), entre dicha posición inicial (HL) y una posición final (HL+BC o HL-BC para CPIR y CPDR).



CPIR:

* Al registro A se le resta el byte contenido en la posición de memoria apuntada por HL.
* El resultado de la resta no se almacena en ningún sitio.
* Los flags resultan afectados por la comparación:
    * Si A==(HL), se pone a 1 el flag de Zero (si no es igual se pone a 0).
    * Si BC==0000, se pone a 0 el flag Parity/Overflow (a 1 en caso contrario).
* Se incrementa HL.
* Se decrementa BC.
* Si BC===0 o A=(HL), se finaliza la instrucción. Si no, repetimos el proceso.



CPDR:
CPDR es, como podéis imaginar, el equivalente a CPIR pero decrementando HL, para buscar hacia atrás en la memoria.

Como ya hemos comentado, muchos flags se ven afectados::

                            Flags 
    Instrucción         |S Z H P N C|
    ----------------------------------
    |CPI                |* * * * 1 -|
    |CPD                |* * * * 1 -|
    |CPIR               |* * * * 1 -|
    |CPDR               |* * * * 1 -|

Un ejemplo de uso de un CP repetitivo es realizar búsquedas de un determinado valor en memoria. Supongamos que deseamos buscar la primera aparición del valor "123" en la memoria a partir de la dirección 20000, y hasta la dirección 30000, es decir, encontrar la dirección de la primera celdilla de memoria entre 20000 y 30000 que contenga el valor 123.

Podemos hacerlo mediante el siguiente ejemplo con CPIR:

.. code-block:: tasm

   LD HL, 20000      ; Origen de la busqueda
   LD BC, 10000      ; Número de bytes a buscar (20000-30000)
   LD A, 123         ; Valor a buscar
   CPIR

Este código realizará lo siguiente::

  HL = 20000
  BC = 10000
  A  = 123

CPIR::
        
    Repetir:
        Leer el contenido de (HL)
        Si A==(HL) -> Fin_de_CPIR
        Si BC==0   -> Fin_de_CPIR
        HL = HL+1
        BC = BC-1
    Fin_de_CPIR:

Con esto, si la celdilla 15000 contiene el valor "123", la instrucción CPIR del ejemplo anterior acabará su ejecución, dejando en HL el valor 15001 (tendremos que decrementar HL para obtener la posición exacta). Dejará además el flag "P/O" (paridad/desbordamiento) y el flag Z a uno. En BC tendremos restado el número de iteraciones del "bucle" realizadas.

Si no se encuentra ninguna aparición de "123", BC llegará a valer cero, porque el "bucle CPI" se ejecutará 10000 veces. El flag P/O estará a cero, al igual que Z, indicando que se finalizó el CPIR y no se encontró nada.

Nótese que si en vez de utilizar CPIR hubiéramos utilizado CPDR, podríamos haber buscado hacia atrás, desde 20000 a 10000, decrementando HL. Incluso haciendo HL=0 y usando CPDR, podemos encontrar la última aparición del valor de A en la memoria (ya que 0000 - 1 = $FFFF, es decir: 0-1=65535 en nuestros 16 bits).


Un ejemplo con CPIR
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



Veamos un ejemplo práctico con CPIR. El código que veremos a continuación realiza una búsqueda de un determinado carácter ASCII en una cadena de texto:

.. code-block:: tasm
            
        ; Principio del programa
        ORG 50000
        
        LD HL, texto     ; Inicio de la busqueda
        LD A, 'X'        ; Carácter (byte) a buscar
        LD BC, 100       ; Número de bytes donde buscar
        CPIR             ; Realizamos la búsqueda
        
        JP NZ, No_Hay    ; Si no encontramos el caracter buscado
        ; el flag de Z estará a cero.
        
        ; Si seguimos por aquí es que se encontró
        DEC HL           ; Decrementamos HL para apuntar al byte
        ; encontrado en memoria.
        
        LD BC, texto
        SCF              
        CCF              ; Ponemos el carry flag a 0 (SCF+CCF)
        SBC HL, BC       ; HL = HL - BC 
                            ;    = (posicion encontrada) - (inicio cadena)
                            ;    = posición de 'X' dentro de la cadena.
        
        LD B, H
        LD C, L          ; BC = HL
        
        RET              ; Volvemos a basic con el resultado en BC
        
    No_Hay:
        LD BC, $FFFF
        RET
        
        texto DB "Esto es una X cadena de texto."
 
        ; Fin del programa
        END 

Lo compilamos con ``pasmo –tapbas buscatxt.asm buscatxt.tap``, lo cargamos en el emulador y tras un RUN ejecutamos nuestra rutina como "PRINT AT 10,10 ; USR 50000". En pantalla aparecerá el valor 12:

Salida del programa buscatxt.asm:



.. figure:: buscatxt.png
   :scale: 80%
   :align: center
   :alt: Salida del programa buscatxt.asm

   Salida del programa buscatxt.asm




¿Qué significa este "12"? Es la posición del carácter 'X' dentro de la cadena de texto. La hemos obtenido de la siguiente forma:

* Hacemos HL = posición de memoria donde empieza la cadena.
* Hacemos A = 'X'.
* Ejecutamos un CPIR
* En HL obtendremos la posición absoluta + 1 donde se encuentra el carácter 'X' encontrado (o FFFFh si no se encuentra). Exactamente 50041.
* Decrementamos HL para que apunte a la 'X' (50040).
* Realizamos la resta de Posicion('X') - PrincipioCadena para obtener la posición del carácter dentro de la cadena. De esta forma, si la 'E' de la cadena está en 50028, y la X encontrada en 50040, eso quiere decir que la 'X' está dentro del array en la posición 50040-50028 = 12.
* Volvemos al BASIC con el resultado en BC. El PRINT USR 50000 imprimirá dicho valor de retorno.

Nótese que el bloque desde "SCF" hasta "LD C, L" tiene como objetivo ser el equivalente a "HL = HL - BC", y se tiene que hacer de esta forma porque no existe "SUB HL, BC" ni "LD BC, HL"::

    SUB HL, BC =  SCF
                  CCF              ; Ponemos el carry flag a 0 (SCF+CCF)
                  SBC HL, BC       ; HL = HL - BC

    LD BC, HL  =  LD B, H
                  LD C, L          ; BC = HL

(Podemos dar las gracias por estas extrañas operaciones a la no ortogonalidad del juego de instrucciones del Z80).


En resumen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



En este capítulo hemos aprendido a utilizar todas las funciones condicionales y de salto de que nos provee el Z80. En el próximo trataremos la PILA (Stack) del Spectrum, gracias a la cual podremos implementar en ensamblador el equivalente a GOSUB/RETURN de BASIC, es decir, subrutinas.

