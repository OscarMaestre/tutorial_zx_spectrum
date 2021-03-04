Lenguaje Ensamblador del Z80 (I)
================================================================================


Arquitectura del Z80 e Instrucciones básicas
--------------------------------------------------------------------------------

En este capítulo explicaremos la sintaxis utilizada en los programas en ensamblador. Para ello comenzaremos con una definición general de la sintaxis para el ensamblador Pasmo, que será el “traductor” que usaremos entre el lenguaje ensamblador y el código máquina del Z80.

Posteriormente veremos en detalle los registros: qué registros hay disponibles, cómo se agrupan, y el registro especial de Flags, enlazando el uso de estos registros con las instrucciones de carga, de operaciones aritméticas, y de manejo de bits, que serán las que trataremos hoy.

Esta entrega del curso es delicada y complicada: por un lado, tenemos que explicar las normas y sintaxis del ensamblador cruzado PASMO antes de que conozcamos la sintaxis del lenguaje ensamblador en sí, y por el otro, no podremos utilizar PASMO hasta que conozcamos la sintaxis del lenguaje.

Además, el lenguaje ensamblador tiene disponibles muchas instrucciones diferentes, y nos resultaría imposible explicarlas todas en un mismo capítulo, lo que nos fuerza a explicar las instrucciones del microprocesador en varias entregas. Esto implica que hablaremos de PASMO comentando reglas, opciones de instrucciones y directivas que todavía no conocemos.

Es por esto que recomendamos al lector que, tras releer anteriores capítulos de este libro, se tome esta entrega de una manera especial, leyéndola 2 veces. La “segunda pasada” sobre el texto permitirá enlazar todos los conocimientos dispersos en el mismo, y que no pueden explicarse de una manera lineal porque están totalmente interrelacionados. Además, la parte relativa a la sintaxis de PASMO será una referencia obligada para posteriores capítulos (mientras continuemos viendo diferentes instrucciones ASM y ejemplos).


Sintaxis del lenguaje ASM en PASMO
--------------------------------------------------------------------------------



En anteriores capítulos ya hablamos de PASMO, el ensamblador cruzado que recomendamos para el desarrollo de programas para Spectrum. Este ensamblador traduce nuestros ficheros de texto .asm con el código fuente de programa (en lenguaje ensamblador) a ficheros .bin (o .tap/.tzx) que contendrán el código máquina directamente ejecutable por el Spectrum.

Supondremos para el resto del capítulo que ya tenéis instalado PASMO (ya sea la versión Windows o la de UNIX/Linux) en vuestro sistema y que sabéis utilizarlo de forma básica (bastará con saber realizar un simple ensamblado de programa, como ya vimos en el primer capítulo), y que podéis ejecutarlo dentro del directorio de trabajo que habéis elegido.

El ciclo de desarrollo con PASMO será el siguiente:

* Con un editor de texto, tecleamos nuestro programa en un fichero .ASM con la sintaxis que veremos a continuación.
* Salimos del editor de texto y ensamblamos el programa:
    * Si queremos generar un fichero .bin de código objeto cuyo contenido POKEar en memoria (o cargar con LOAD “” CODE) desde un cargador BASIC, lo ensamblamos con: “pasmo ejemplo1.asm ejemplo1.bin”
    * Si queremos generar un fichero .tap directamente ejecutable (de forma que sea pasmo quien añada el cargador BASIC), lo ensamblamos con “pasmo –tapbas ejemplo1.asm ejemplo1.tap”

Todo esto se mostró bastante detalladamente en su momento en el primer capítulo del curso.

Con esto, ya sabemos ensamblar programas creados adecuadamente, de modo que la pregunta es: ¿cómo debo escribir mi programa para que PASMO pueda ensamblarlo?

Es sencillo: escribiremos nuestro programa en un fichero de texto con extensión .asm. En este fichero de texto se ignorarán las líneas en blanco y los comentarios, que en ASM de Z80 se introducen con el símbolo “;” (punto y coma), de forma que todo lo que el ensamblador encuentre a la derecha de un ; será ignorado (siempre que no forme parte de una cadena). Ese fichero de texto será ensamblado por PASMO y convertido en código binario.

Lo que vamos a ver a continuación son las normas que debe cumplir un programa para poder ser ensamblado en PASMO. Es necesario explicar estas reglas para que el lector pueda consultarlas en el futuro, cuando esté realizando sus propios programas. No te preocupes si no entiendes alguna de las reglas, cuando llegues al momento de implementar tus primeras rutinas, las siguientes normas te serán muy útiles:



* Normas para las instrucciones:
    * Pondremos una sóla instrucción de ensamblador por línea.
    * Como existen diferencias entre los “fin de línea” entre Linux y Windows, es recomendable que los programas se ensamblen con PASMO en la misma plataforma de S.O. en que se han escrito. Si PASMO intenta compilar en Windows un programa ASM escrito en un editor de texto de Linux (con retornos de carro de Linux) es posible que obtengamos errores de ensamblado (aunque no es seguro). * Si os ocurre al compilar los ejemplos que os proporcionamos (están escritos en Linux) y usáis Windows, lo mejor es abrir el fichero .ASM con notepad y grabarlo de nuevo (lo cual lo salvará con formato de retornos de carro de Windows). El fichero “regrabado” con Notepad podrá ser ensamblado en Windows sin problemas.
    * Además de una instrucción, en una misma línea podremos añadir etiquetas (para referenciar a dicha línea, algo que veremos posteriormente) y comentarios (con ';').


* Normas para los valores numéricos:
    * Todos los valores numéricos se considerarán, por defecto, escritos en decimal.
    * Para introducir valores números en hexadecimal los precederemos del carácter “$”, y para escribir valores numéricos en binario lo haremos mediante el carácter “%”.
    * Podremos también especificar la base del literal poniendoles como prefijo las cadena &H ó 0x (para hexadecimal) o &O (para octal).
    * Podemos especificar también los números mediante sufijos: Usando una “H” para hexadecimal, “D” para decimal, “B” para binario u “O” para octal (tanto mayúsculas como minúsculas).


* Normas para cadenas de texto:
    * Podemos separar las cadenas de texto mediante comillas simples o dobles.
    * El texto encerrado entre comillas simples no recibe ninguna interpretación, excepto si se encuentran 2 comillas simples consecutivas, que sirven para introducir una comilla simple en la cadena.
    * El texto encerrado entre comillas dobles permite introducir caracteres especiales al estilo de C/C++ como \n, \r o \t (nueva línea, retorno de carro, tabulador…).
    * El texto encerrado entre comillas dobles también admite \xNN para introducir el carácter correspondiente a un número hexadecimal NN.
    * Una cadena de texto de longitud 1 (un carácter) puede usarse como una constante (valor ASCII del carácter) en expresiones como, por ejemplo, 'C'+10h.


* Normas para los nombres de ficheros:
    * Si vemos que nuestro programa se hace muy largo y por lo tanto incómodo para editarlo, podemos partir el fichero en varios ficheros e incluirlos mediante directivas INCLUDE (para incluir ficheros ASM) o INCBIN (para incluir código máquina ya compilado). Al especificar nombres de ficheros, deberán estar entre dobles comillas o simples comillas.


* Normas para los identificadores:
    * Los identificadores son los nombres usados para etiquetas y también los símbolos definidos mediante EQU y DEFL.
    * Podemos utilizar cualquier cadena de texto, excepto los nombres de las palabras reservadas de ensamblador.


* Normas para las etiquetas:
    * Una etiqueta es un identificador de texto que ponemos poner al principio de cualquier línea de nuestro programa, por ejemplo: “bucle:”
    * Podemos añadir el tradicional sufijo “:” a las etiquetas, pero también es posible no incluirlo si queremos compatibilidad con otros ensambladores que no lo soporten (por si queremos ensamblar nuestro programa con otro ensamblador que no sea pasmo).
    * Para PASMO, cualquier referencia a una etiqueta a lo largo del programa se convierte en una referencia a la posición de memoria de la instrucción o dato siguiente a donde hemos colocado la etiqueta. Podemos utilizar así etiquetas para hacer referencia a nuestros gráficos, variables, datos, funciones, lugares a donde saltar, etc.


* Directivas:
    * Tenemos a nuestra disposición una serie de directivas para facilitarnos la programación, como DEFB o DB para introducir datos en crudo en nuestro programa, ORG para indicar una dirección de inicio de ensamblado, END para finalizar el programa e indicar una dirección de autoejecución, IF/ELSE/ENDIF en tiempo de compilación, INCLUDE e INCBIN, MACRO y REPT.
    * La directiva END permite indicar un parámetro numérico (END XXXX) que “pasmo –tapbas” toma para añadir al listado BASIC de arranque el RANDOMIZE USR XXXX correspondiente. De esta forma, podemos hacer que nuestros programas arranquen en su posición correcta sin que el usuario tenga que teclear el “RANDOMIZE USR DIRECCION_INICIO”.

* Una de las directivas más importantes es ORG, que indica la posición origen donde almacenar el código que la sigue. Podemos utilizar diferentes directivas ORG en un mismo programa. Los datos o el código que siguen a una directiva ORG son ensamblados a partir de la dirección que indica éste.
* Iremos viendo el significado de las directivas conforme las vayamos usando, pero es aconsejable consultar el manual de PASMO para conocer más sobre ellas.


* Operadores
    * Podemos utilizar los operadores típicos +, -, \*. /, así como otros operadores de desplazamiento de bits como » y «.
    * Tenemos disponibles operadores de comparación como EQ, NE, LT, LE, GT, GE o los clásicos =, !=, <, >, ⇐, >=.
    * Existen también operadores lógicos como AND, OR, NOT, o sus variantes \&, \|, \!.
    * Los operadores sólo tienen aplicación en tiempo de ensamblado, es decir, no podemos multiplicar o dividir en tiempo real en nuestro programa usando * o /. Estos operadores están pensados para que podamos poner expresiones como ((32*10)+12), en lugar del valor numérico del resultado, por ejemplo.


Aspecto de un programa en ensamblador

Veamos un ejemplo de programa en ensamblador que muestra el uso de algunas de estas normas, para que las podamos entender fácilmente mediante los comentarios incluidos:

.. code-block:: tasm

    ; Programa de ejemplo para mostrar el aspecto de
    ; un programa típico en ensamblador para PASMO.
    ; Copia una serie de bytes a la videomemoria con
    ; instrucciones simples (sin optimizar).
    ORG 40000
        
    valor     EQU  1
    destino   EQU  18384
        
        ; Aqui empieza nuestro programa que copia los
        ; 7 bytes desde la etiqueta "datos" hasta la
        ; videomemoria ([16384] en adelante).
        
        LD HL, destino     ; HL = destino (VRAM)
        LD DE, datos       ; DE = origen de los datos
        LD B, 6            ; numero de datos a copiar
        
    bucle:               ; etiqueta que usaremos luego
        
        LD A, (DE)         ; Leemos un dato de [DE]
        ADD A, valor       ; Le sumamos 1 al dato leído
        LD (HL), A         ; Lo grabamos en el destino [HL]
        INC DE             ; Apuntamos al siguiente dato
        INC HL             ; Apuntamos al siguiente destino
        
        DJNZ bucle         ; Equivale a:
                            ; B = B-1
                            ; if (B>0) goto Bucle
        RET
        
    datos DEFB 127, %10101010, 0, 128, $FE, %10000000, FFh
        
    END

Algunos detalles a tener en cuenta:

* Se utiliza una instrucción por línea.
* Los comentarios pueden ir en sus propias líneas, o dentro de líneas de instrucciones (tras ellas).
* Podemos definir “constantes” con EQU para hacer referencia a ellas luego en el código. Son constantes, no variables, es decir, se definen en tiempo de ensamblado y no se cambian con la ejecución del programa. Su uso está pensado para poder escribir código más legible y que podamos cambiar los valores asociados posteriormente de una forma sencilla (es más fácil cambiar el valor asignado en el EQU, que cambiar un valor en todas sus apariciones en el código).
* Podemos poner etiquetas (como “bucle” y “datos” -con o sin dos puntos, son ignorados-) para referenciar a una posición de memoria. Así, la etiqueta “bucle” del programa anterior hace referencia a la posición de memoria donde se ensamblaría la siguiente instrucción que aparece tras ella. Las etiquetas se usan para poder saltar a ellas (en los bucles y condiciones) mediante un nombre en lugar de tener que calcular nosotros la dirección del salto a mano y poner direcciones de memoria. Es más fácil de entender y programar un “JP bucle” que un “JP $40008”, por ejemplo. En el caso de la etiqueta “datos”, nos permite referenciar la posición en la que empiezan los datos que vamos a copiar.
* Los datos definidos con DEFB pueden estar en cualquier formato numérico, como se ha mostrado en el ejemplo: decimal, binario, hexadecimal tanto con prefijo “$” como con sufijo “h”, etc.

Podéis ensamblar el ejemplo anterior mediante::

    pasmo --tapbas ejemplo.asm ejemplo.tap

Una vez cargado y ejecutado el TAP en el emulador de Spectrum, podréis ejecutar el código máquina en BASIC con un “RANDOMIZE USR 40000”, y deberéis ver una pantalla como la siguiente: 



.. figure:: ejemplo1.png
   :scale: 80%
   :align: center
   :alt: 

   


