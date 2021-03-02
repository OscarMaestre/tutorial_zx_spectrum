Introducción y conceptos básicos
======================================

Los límites de BASIC
----------------------------------

Todo aquel lector que haya programado en BASIC conocerá sin duda la principal limitación de este sencillo lenguaje de alto nivel: es lento, muy lento. A cambio de su sencillez pagamos una penalización enorme en velocidad.

BASIC es un lenguaje interpretado, lo que quiere decir que el Spectrum (más bien el intérprete BASIC integrado en la ROM) tiene que leer línea a línea nuestro programa, decodificar lo que estamos diciendo en lenguaje BASIC, traducirlo a instrucciones comprensibles por el procesador y ejecutarlo, todo ello en tiempo real.

Eso implica que cada vez que se ejecuta el programa BASIC, para cada línea del programa se ejecuta un proceso de lectura, decodificación, traducción y ejecución. Este proceso es lento e implica que no sólo se está ejecutando nuestro programa sino que debajo de él tenemos al intérprete de BASIC realizando todas estas tareas y restándonos parte de la potencia de CPU del Spectrum, que ya de por sí no es especialmente potente.

No importa lo elegantemente optimizado que esté nuestro programa en BASIC, el proceso de interpretación en sí hará que se ejecute con una lentitud que no podemos salvar.

BASIC tiene una serie de trucos más o menos conocidos para acelerar su ejecución: escribir muchas instrucciones en una sóla línea BASIC, poner las rutinas que más velocidad necesitan en las primeras líneas de programa, reducir el nombre (en longitud) de las variables, etc. Pero al final llegamos a un punto en que no podemos mejorar nuestros programas en cuanto a velocidad. 


.. figure:: basic.gif
   :scale: 80 %
   :alt: El editor del intérprete de BASIC

   El editor del intérprete de BASIC



    Revisiones antiguas
    Enlaces a esta página
    Exportación a ODT

Tabla de Contenidos
Introducción y conceptos básicos


Los límites de BASIC

Todos aquel lector que haya programado en BASIC conocerá sin duda la principal limitación de este sencillo lenguaje de alto nivel: es lento, muy lento. A cambio de su sencillez pagamos una penalización enorme en velocidad.

BASIC es un lenguaje interpretado, lo que quiere decir que el Spectrum (más bien el intérprete BASIC integrado en la ROM) tiene que leer línea a línea nuestro programa, decodificar lo que estamos diciendo en lenguaje BASIC, traducirlo a instrucciones comprensibles por el procesador y ejecutarlo, todo ello en tiempo real.

Eso implica que cada vez que se ejecuta el programa BASIC, para cada línea del programa se ejecuta un proceso de lectura, decodificación, traducción y ejecución. Este proceso es lento e implica que no sólo se está ejecutando nuestro programa sino que debajo de él tenemos al intérprete de BASIC realizando todas estas tareas y restándonos parte de la potencia de CPU del Spectrum, que ya de por sí no es especialmente potente.

No importa lo elegantemente optimizado que esté nuestro programa en BASIC, el proceso de interpretación en sí hará que se ejecute con una lentitud que no podemos salvar.

BASIC tiene una serie de trucos más o menos conocidos para acelerar su ejecución: escribir muchas instrucciones en una sóla línea BASIC, poner las rutinas que más velocidad necesitan en las primeras líneas de programa, reducir el nombre (en longitud) de las variables, etc. Pero al final llegamos a un punto en que no podemos mejorar nuestros programas en cuanto a velocidad.


Lenguaje BASIC y su intérprete
El editor del intérprete de BASIC


Para muchos, el BASIC del Spectrum es un comienzo prácticamente obligado para programar, pero si queremos realizar programas con la calidad del software comercial no puede ser la herramienta a utilizar. Dejando de lado que sigue siendo una herramienta muy útil para programar en el Spectrum, para muchos llega la hora de dar el siguiente paso. 


Alternativas a BASIC
==================================


Aparte de realizar programas para el intérprete de BASIC existen múltiples alternativas para programar juegos y aplicaciones que expriman al máximo nuestra máquina: 


Subrutinas en ensamblador dentro de un programa BASIC
----------------------------------------------------------

Para empezar, como primera opción, podemos realizar pequeñas rutinas en ensamblador y utilizarlas desde nuestros programas en BASIC. El lenguaje ensamblador se trata del lenguaje más cercano a lo que es el código binario que entiende directamente un microprocesador. Es de bajo nivel, es decir, está más lejos del lenguaje humano de lo que está BASIC, y a la vez está muy cerca del lenguaje que entiende el microprocesador de nuestro Spectrum.

En BASIC, una instrucción es traducida por el intérprete BASIC a una serie más o menos larga de comandos en lenguaje máquina. Por ejemplo, 10 PRINT "HOLA", se traduce como una serie de comandos en lenguaje máquina que podrían ser algo como "para cada una de las letras de la palabra HOLA, realiza todas las operaciones necesarias para mostrar en pantalla todos los píxels que forman dichas letras, actualizando la posición del cursor y usando el color INK y PAPER actual".

Una instrucción BASIC equivale a una gran cantidad de instrucciones en código máquina.

Por contra, una instrucción en lenguaje ensamblador equivale a una sóla instrucción en lenguaje máquina: hablamos directamente el lenguaje de la máquina, sólo que en vez de hacerlo con unos y ceros, lo hacemos en un lenguaje que tiene unas determinadas reglas de sintaxis y que el "programa ensamblador" se encarga de traducir a código máquina. Es por eso que programar en ensamblador es de "bajo nivel": hablamos directamente al nivel de la máquina, y por eso mismo los programas son más complicados de escribir, de leer y de mantener que un programa en BASIC, donde se habla un lenguaje más natural y que es traducido a lo que la máquina entiende. 

.. code-block:: tasm

    ;
    ; Rutina de multiplicación en lenguaje ensamblador:
    ;
    ; MULTIPLICA: Multiplica DE*BC
    ;
    ;       Entrada:        DE: Multiplicando,  
    ;                       BC: Multiplicador
    ;       Salida:         HL: Resultado.
    
    MULTIPLICA:
            LD HL, 0            ; HL = 0
    MULTI01:
            ADD HL, DE          ; Sumamos HL = HL + DE
            DEC BC
            LD A, B
            OR C
            JR NZ, MULTI01      ; Lo repetimos BC veces
            RET                 ; Volver de la rutina


La primera de las opciones que estamos tratando, la de programar rutinas en ensamblador y utilizarlas después desde programas en BASIC seguiría el siguiente ciclo de desarrollo:


* Programamos una rutina en lenguaje ensamblador que realice una función concreta: por ejemplo, dibujar el personaje o enemigos de nuestro juego, borrar la pantalla, actualizar los marcadores, etc.
* Ensamblamos la rutina con un programa ensamblador y obtenemos un bloque de datos que contiene la traducción del programa que hemos escrito a código máquina directamente comprensible por el microprocesador.
* Cargamos en memoria el bloque de datos de código máquina que acabamos de obtener mediante un LOAD "" CODE o POKEando cada byte de este bloque de datos en memoria.
* Programamos nuestro programa en BASIC, y llamamos a la rutina que hemos programando cuando la necesitemos utilizando RANDOMIZE USR hacia la dirección en que hemos cargado o POKEado la rutina.


Es decir: realizamos una rutina o un conjunto de rutinas en ensamblador y mediante un programa ensamblador, traducimos el código ASM a código que entiende directamente la máquina (código binario) y lo salvamos en cinta (o si es corto, anotamos sus valores para meterlos en DATAs). Después, al inicio de nuestro programa, introducimos ese código binario en memoria de forma que lo podamos llamar en cualquier momento desde BASIC con RANDOMIZE USR.

Esto permite realizar rutinas importantes y críticas en lenguaje ensamblador, y mantener el esqueleto del programa principal en BASIC. Las rutinas creadas en ensamblador son llamadas desde BASIC con la instrucción **USR** en aquellos puntos del programa en que las necesitemos.

Más adelante en este capítulo veremos un ejemplo de cómo realizar el ensamblado de una rutina en ensamblador, su carga en memoria y su utilización desde un programa en BASIC.

Compilando el programa BASIC con un compilador
--------------------------------------------------

Aunque utilicemos rutinas en ensamblador llamadas desde BASIC, seguiremos lastrados por la velocidad del intérprete y los tiempos de ejecución de las partes del programa que no están escritas en ensamblador.

Como una segunda opción alternativa a la integración BASIC-ASM, tenemos la opción de utilizar un compilador de BASIC para compilar nuestros programas y traducirlos a código máquina sin pasar por ningún intérprete de BASIC.

Mediante un compilador de BASIC, a partir de un programa de código fuente en BASIC obtenemos un ejecutable que podremos cargar directamente en memoria y ejecutarlo sin necesidad de utilizar el intérprete del sistema.

La labor de interpretación del código BASIC se hace igualmente, pero se hace antes, ya que en lugar de ejecutar, el resultado de la interpretación se graba ya "traducido" en cinta. Un programa en BASIC compilado y ejecutado de este modo es muchísimo más rápido que el mismo programa ejecutado en el intérprete de BASIC del Spectrum.

**MCODER**, uno de los compiladores nativos de BASIC más conocidos, es una buena solución, y para muchos puede ser suficiente para muchas de sus creaciones. Nuestra querida DINAMIC realizó sus primeros juegos en BASIC con MCODER: hablamos de Babaliba, Saimazoom, o la utilidad Artist. MCODER tiene unas limitaciones que no tienen porqué ser especialmente problemáticas si las conocemos, las aceptamos, y realizamos nuestros programas teniéndolas en cuenta. Por ejemplo, no podemos utilizar vectores (creados con DIM en BASIC), y el manejo de cadenas sufre algunos cambios de sintaxis, entre otros.

La principal desventaja de MCODER es que es un compilador BASIC nativo, es decir, que es software para Spectrum que debemos ejecutar dentro de un emulador o la máquina real lo que nos puede ralentizar a la hora de programar.

Una opción mucho más aconsejable es la de utilizar un compilador cruzado como **ZX Basic Compiler** (ZXB Compiler).

Un **compilador cruzado** es un compilador que se ejecuta en una plataforma diferente de la plataforma destino, pero genera código para ésta. Por ejemplo, podemos escribir nuestro programa BASIC en un editor de textos en un PC (fuera del Spectrum), compilarlo con un compilador cruzado, y obtener un binario con código máquina de Spectrum, listo para ser ejecutado en un emulador o en una máquina real. De esta forma nos beneficiamos de las mayores capacidades de nuestra plataforma de desarrollo (un PC) para conseguir código compilado para un Spectrum.

En este caso, el compilador cruzado ZX Basic Compiler permite compilar programas escritos en un dialecto BASIC estándar y genera un fichero de instrucciones en ensamblador que podemos ensamblar con ensambladores cruzados.

El ciclo de desarrollo para la compilación de programas BASIC sería similar al siguiente:


* Programamos nuestro juego en lenguaje BASIC escribiendo el programa en un editor de textos estándar de nuestra plataforma de desarrollo.
* Grabamos el código de nuestro programa como un fichero .BAS.
* Mediante el compilador cruzado, compilamos el fichero .BAS y obtenemos un fichero binario de código máquina, normalmente con un cargador BASIC incluído al principio del mismo.
* Cargamos ese código máquina en nuestro Spectrum o emulador con un simple LOAD "".
* El programa se carga y ejecuta como cualquier otro juego comercial.


Es una opción muy interesante para quien quiera seguir programando en BASIC y obtener la potencia que el intérprete de BASIC le resta. 






Programando en Lenguaje C
-------------------------------

Otra opción es la de aprender lenguaje C y realizar programas íntegramente en C que son compilados (al igual que hace ZX Basic Compiler) y trasladados a código binario que ejecutará el Spectrum.

Podemos ver el lenguaje C (en el Spectrum) como una manera de realizar programas bastante rápidos saltándonos las limitaciones de BASIC. No llega a ser ensamblador, pero desde luego es mucho más rápido que BASIC (y que BASIC compilado).

C es un lenguaje muy potente y de alto nivel que genera un código bastante óptimo y cuyos binarios tienen una velocidad de ejecución muchísimo más cercana a la de programas en ensamblador que a la de programas BASIC interpretados.

El desarrollo de un juego o programa en C se realizaría de forma similar al caso de los compiladores BASIC:


* Programamos nuestro juego en lenguaje C escribiendo el programa en un editor de textos estándar de nuestra plataforma de desarrollo.
* Grabamos el código de nuestro programa como un fichero .C .
* Mediante el compilador cruzado, compilamos el fichero .C y obtenemos un fichero binario de código máquina, normalmente con un cargador BASIC incluído al principio del mismo.
* Cargamos ese código máquina en nuestro Spectrum o emulador con un simple LOAD "".
* El programa se carga y ejecuta como cualquier otro juego comercial.


Para quien ya conozca el lenguaje C y se desenvuelva bien con él, utilizar un compilador cruzado como pueda serlo Z88DK será sin duda un gran opción. Programando en C se puede hacer prácticamente cualquier aplicación y un gran número de juegos.

Además, se puede embeber código ensamblador dentro de las rutinas en C, con lo cual se puede decir que no estamos limitados por el lenguaje C a la hora de realizar tareas que requieren un control muy preciso de la máquina.


Realizando el programa completo en ensamblador.
-----------------------------------------------------

Finalmente, la última opción: nos hemos decidido y queremos escribir programas directamente en el lenguaje que comprende la máquina, ya que queremos controlar todo lo que realiza el microprocesador.

Con la opción que hemos elegido, escribiremos el código del programa íntegramente en lenguaje ensamblador (assembler language en inglés, o ASM para abreviar).

Con BASIC compilado y con C, es el compilador quien transforma nuestros comandos en código máquina. En el lenguaje ensamblador, la "compilación" (conocida como proceso de ensamblado) del programa en código máquina es una mera traducción ya que cada instrucción en ensamblador se traduce en una instrucción en código máquina, como veremos más adelante.

Para programar en ensamblador seguiremos el siguiente proceso:


* Programamos nuestro juego en lenguaje ensamblador escribiendo el programa en un editor de textos estándar de nuestra plataforma de desarrollo.
* Grabamos el código de nuestro programa como un fichero .ASM .
* Mediante el ensamblador cruzado, ensamblamos el fichero .ASM y obtenemos un fichero binario de código máquina, normalmente con un cargador BASIC incluído al principio del mismo.
* Cargamos ese código máquina en nuestro Spectrum o emulador con un simple LOAD "".
* El programa se carga y ejecuta como cualquier otro juego comercial.


Es importante destacar que el desarrollo de un programa en ASM requiere mucho más tiempo, un mejor diseño y muchos más conocimientos del hardware que utilizar cualquier otro lenguaje. Un programa en BASIC sencillo puede tener 1000 líneas, pero el mismo programa en ASM puede tener perfectamente 10000, 50000, o muchas más líneas.

En ensamblador no tenemos funciones de alto nivel que realicen determinadas tareas por nosotros: no existe PRINT para imprimir cosas por pantalla, si queremos imprimir texto tenemos que imprimir una a una las letras, calculando posiciones, píxeles, colores, y escribiendo en la videomemoria nosotros mismos. Podemos apoyarnos en una serie de rutinas que hay en la ROM del Spectrum (que son las que utiliza BASIC), pero en general, para la mayoría de las tareas, lo tendremos que hacer todo manualmente.

Un ejemplo muy sencillo: en BASIC podemos multiplicar 2 números de forma muy simple con el operador "*". En ensamblador, no existe un comando para multiplicar 2 números. No existe dicho comando porque el micro Z80 tiene definida la operación de suma (ADD) y la de resta (SUB), por ejemplo, pero no tiene ninguna instrucción para multiplicar o dividir. Y si queremos multiplicar 2 números, tendremos que hacer una rutina en ensamblador que lo haga (como la rutina que hemos visto en el apartado anterior) y llamarla cada vez que necesitemos realizar una multiplicación.

Es posible que el anterior párrafo parezca demasiado "duro" para los programadores acostumbrados a BASIC y que lo anteriormente explicado parezca un panorama desolador, pero esa es la realidad con el ensamblador: cada instrucción en ensamblador se corresponde con una instrucción de la CPU Z80. Si se quiere hacer algo más complejo que lo que permite directamente la CPU, nos lo hemos de construir nosotros mismos a base de utilizar esas instrucciones. Una multiplicación se puede realizar como una serie de sumas, por ejemplo, como hemos visto en la rutina MULT del apartado anterior.

Descrito visualmente, en BASIC para construir una casa te dan paredes completas, ventanas, escaleras y puertas, y combinándolos te construyes la casa. En ASM, por contra, lo que te dan es un martillo, clavos, un cincel, madera y roca, y a partir de eso tienes que construir tú todos los elementos del programa.

Obviamente, no tendremos que escribir miles de rutinas antes de poder programar cualquier cosa: existen rutinas ya disponibles que podemos aprovechar. En Internet, en revistas Microhobby, en libros de programación de Z80, en la ROM del Spectrum, encontraremos rutinas listas para utilizar y que nos permitirán multiplicar, dividir, imprimir cadenas de texto, y muchas otras cosas.

Además, cada nueva rutina que programemos podremos reutilizarla en futuros programas, por lo que el inicio es duro pero a partir de cierto momento dispondremos de bibliotecas de rutinas que podremos integrar en nuestros programas para reducir el tiempo de desarrollo.




Por qué aprender ASM (ensamblador) de Z80
==============================================

Está claro que cada lenguaje tiene su campo de aplicación, y utilizar BASIC para hacer una herramienta interactiva para el usuario (con mucho tratamiento de textos, o de gráficos) o bien para hacer un programa basado en texto, o una pequeña base de datos o similar puede ser suficiente para muchos casos.

Donde realmente tiene interés la programación en lenguaje ensamblador es en la creación de determinadas rutinas, programas o juegos orientados a exprimir el hardware de la máquina, es decir: aquellos programas orientados a escribir rápidamente gráficos en pantalla, reproducir música, o controlar el teclado con gran precisión. Nos estamos refiriendo principalmente a los juegos.

Ensamblador es el lenguaje ideal para programar juegos que requieran gran velocidad de ejecución. Como veremos en el futuro, dibujar en pantalla se reduce a escribir valores en memoria (en una zona concreta de la memoria). Leer del teclado se reduce a leer los valores que hay en determinados puertos de entrada/salida de la CPU, y la reproducción de música se realiza mediante escrituras en otros puertos. Para realizar esto se requiere mucha sincronización y un control total de la máquina, y esto es lo que nos ofrece ensamblador.

Este curso está diseñado con los siguientes objetivos en mente:


* Conocer el hardware del Spectrum, y cómo funciona internamente.
* Conocer el juego de instrucciones del microprocesador Z80 que lleva el Spectrum.
* Saber realizar programas en lenguaje ASM (ensamblador) del Z80.
* Aprender a realizar pequeñas rutinas que hagan tareas determinadas y que sean después reutilizables desde otros programas o desde BASIC.
* Con la práctica, ser capaces de escribir un juego o programa entero en ASM.


Proporcionaremos al lector todos los conceptos necesarios para conseguir estos objetivos. El resto lo aportará el tiempo que nos impliquemos y la experiencia que vayamos adoptando programando en ensamblador. No se puede escribir un juego completo en ensamblador la primera vez que uno se acerca a este lenguaje, pero sí que puede uno realizar una pequeña rutina que haga una tarea concreta en un pequeño programa BASIC. La segunda vez, en lugar de una pequeña rutina hará un conjunto de rutinas para un juego mayor, y, con la práctica, el dominio del lenguaje se puede convertir para muchos en una manera diferente o mejor de programar: directamente en ensamblador.

Queremos destacar un pequeño detalle: programar en ensamblador no es fácil. Este curso deberían seguirlo aquellas personas con ciertos conocimientos sobre programación que se sientan preparadas para dar el paso al lenguaje ensamblador. Si tienes conocimientos de hardware, sabes cómo funciona un microprocesador, has realizado uno o más programas o juegos en BASIC u otros lenguajes o sabes lo que es binario, decimal y hexadecimal (si sabes cualquiera de esas cosas), entonces no te costará nada seguir este curso. Si, por el contrario, no has programado nunca, y todo lo que hemos hablado no te suena de nada, necesitarás mucha voluntad y consultar muchos otros textos externos (o al menos aplicarte mucho) para poder seguirnos.

Un requerimiento casi imprescindible es que el lector debe de conocer fundamentos básicos del sistema de codificación decimal, hexadecimal y binario. Como ya sabéis, nosotros expresamos los números en base decimal, pero esos mismos números se pueden expresar también en hexadecimal, o en binario. Son diferentes formas de representar el mismo número, y para distinguir unas formas de otras se colocan prefijos o sufijos que nos indican la base utilizada. A lo largo del curso se utilizarán las siguientes convenciones de prefijo de formato: 

==========  ====================
Prefijo      Tipo de dato      
==========  ====================
 $           Valor hexadecimal 
 %           Valor en binario 
 Ninguno     Valor en decimal 
==========  ====================


Para seguir el curso es muy importante que el lector sepa distinguir unas bases de codificación de otras y que sepa (con más o menos facilidad) pasar números de una base a otra. Quien no sepa esto lo puede hacer con práctica, conforme va siguiendo el curso. 

============ ============   ===========
DECIMAL       HEXADECIMAL    BINARIO
============ ============   ===========
64d ó 64      $40 ó 40h 	 %01000000
255d ó 255    $FF ó FFh 	 %11111111
3d ó 3        $03 ó 03h      %00000011 
============ ============   ===========



El código máquina del microprocesador Z80
==========================================================


El microprocesador Z80 (Z80A en el caso del Spectrum) es un pequeño chip de 40 pines de conexión, cada uno de las cuales está conectada a diferentes señales. Uno de los pines es la alimentación eléctrica, otro la conexión al reloj/cristal de 3.50Mhz, 8 pines suponen el bus de datos y 16 el bus de direcciones, etc. 


.. figure:: z80a.jpg
   :scale: 80 %
   :alt: El microprocesador Z80

   El microprocesador Z80




Estas "patillas" de datos y direcciones están físicamente conectadas a través de pistas eléctricas a la memoria, el teclado, el cassette, etc. Utilizando las patillas de direcciones el procesador selecciona "posiciones de memoria" en la memoria, y recibe las instrucciones de los programas a través de las 8 señales del bus de datos.

Una señal (el estado de cada una de las patillas del micro en un instante concreto) puede tener 2 estados: sin tensión eléctrica (0 Voltios físicos, o señal lógica "0"), o con tensión eléctrica (5 Voltios físicos, o señal lógica "1"). El procesador recibe a través de las 8 patillas del bus de datos 8 señales que conforman una ristra de unos y ceros como puedan serlo 01000100 o 11001100, por ejemplo.

Los diseñadores del Z80 le otorgaron mediante circuitos en su interior una serie de registros de almacenamiento (A, B, C, D, E, F, H, L, etc.) que pueden alojar números, y la capacidad de ejecutar una serie de instrucciones (sumar, restar, comparar, etc.) entre ellos (y también entre ellos y otras posiciones de memoria).

Cada posible conjunto de señales entre 00000000 y 11111111 se corresponde con una de estas posibles operaciones mediante un "diccionario interno" que le dice al Z80 qué debe de hacer según la instrucción que se le está solicitando.

Cuando el microprocesador obtiene de la memoria la siguiente instrucción del programa a ejecutar y obtiene, por ejemplo, un conjunto de señales "01010000", el Z80 sabe que tiene que sumar el contenido de su registro interno A con el del registro interno B, y dejar el resultado en A.

Es decir, entiende un número binario de 8 digítos que recibe en forma de señales binarias como una instrucción concreta a ejecutar. Este valor numérico es lo que se conoce como un **"Opcode"** o **"código de operación"**, ya que un código (01010000) le indica al procesador qué operación ejecutar (A = A + B). 


Un programa en código máquina no es más que una ristra de código binarios de 8 dígitos (de instrucciones) que le indican al Z80 qué operaciones ejecutar en un orden concreto. El procesador leerá una a una la ristra de códigos binarios que forman el programa y ejecutará cada una de las instrucciones con que se corresponde cada código.

El Z80 utiliza un registro interno especial llamado PC (Program Counter o Contador de Programa) para saber cuál es la dirección de la instrucción actual con la que está trabajando y lo incrementa tras cada instrucción para poder seguir el flujo del programa.

Cuando arrancamos nuestro Spectrum, todos los registros del Z80 (A, B, C, PC, etc) valen 0, por lo que el Spectrum empieza a leer desde la memoria en la posición 0, instrucción tras instrucción, incrementando el valor de PC tras ejecutar cada una de ellas. Este programa "inicial" que ejecuta nuestro Spectrum es nada más y nada menos que el intérprete de BASIC, escrito para Sinclair por ingenierios de Nine Tiles Information Handlind Ltd.

Este código máquina con todo el programa que supone el intérprete BASIC está almacenado como ristra de instrucciones en un chip del Spectrum llamado ROM cuyo contenido no se borra al apagar el ordenador.

Programar en código máquina no es fácil, puesto que no es inmediata la correspondencia entre una ristra de unos y ceros y la instrucción que ejecutará el procesador. Una vez escrito un programa, es también muy complicado de depurar en busca de errores, puesto que todo lo que tenemos son miles o decenas de miles de ristras de 8 dígitos binarios.

Veamos algunas instrucciones en código máquina y el efecto que tienen en el procesador cuando le pedimos ejecutarlas: 

==========================  ==================================   ==============================
Instrucción en hexadecimal  Señales en bus de datos (binario)    Instrucción ejecutada
==========================  ==================================   ==============================
$09                                   00001001                        HL = HL + BC
$50                                   01010000                        A = A + B
$3C                                   00111100                        Incrementar A ; A = A + 1
$3D                                   00111101                        Decrementar A ; A = A - 1
==========================  ==================================   ==============================




 El conjunto completo de operaciones que puede realizar el procesador representado por los opcodes asociados a los mismos se conoce como **juego de instrucciones del procesador**.

Recordar todos los códigos de operación del juego de instrucciones es muy complejo y la programación en base a utilizar ristras de números es prácticamente inmanejable. Debido a esta complejidad y dificultad, nunca se programa directamente en código máquina sino que se realiza en **lenguaje ensamblador**. 



El lenguaje ensamblador
============================

El lenguaje ensamblador es una "versión humana" del lenguaje máquina en la que asociamos un "nombre" (técnicamente conocido como mnenónico) a cada instrucción de 8 bits del procesador.

Así, en lugar de definir la suma de A = A + B como **"001010000"**, la definimos como **"ADD A, B"**, lo cual es mucho más legible e intuitivo a la hora de programar y depurar y sigue siendo igual de compacto, existiendo una correspondencia exacta de 1 instrucción ASM = 1 instrucción en código máquina.

De esta forma, podemos programar utilizando un conjunto de instrucciones en lenguaje "humano", que no llegan a ser tan especializadas y de tanto alto nivel como en BASIC ya que el objetivo del lenguaje ensamblador es dotar de un nombre "legible" a cada microinstrucción disponible en el procesador.

Al programar en lenguaje ensamblador, lo hacemos pues en este lenguaje humano con instrucciones como "ADD A, B", "LD A, 20" o "CALL subrutina". El problema es que el microprocesador no entiende este lenguaje humano, ya que él sólo entiende las señales de 8 dígitos binarios que lee de la memoria.

Para solucionar esto se necesita un programa llamado **"programa ensamblador"** o simplemente **ensamblador** o **assembler**, que lee nuestros programas en lenguaje ensamblador y convierte cada instrucción en ensamblador en la correspondiente instrucción código máquina. El resultado de la conversión de cada instrucción se va almacenando de forma consecutiva para acabar obteniendo un bloque de datos que contiene la traducción a código máquina de todo el programa que hemos solicitado ensamblar.

Para realizar este proceso, el programa ensamblador se vale de una tabla de ensamblado que relaciona cada instrucción en ensamblador con la instrucción en código máquina que realiza la misma acción. Así, cuando lee en nuestro programa "ADD A, B", lo traduce por un "001010000" que es lo que realmente almacena en el programa en código máquina resultante.

En resumen: como resultado de un proceso de ensamblado, el ensamblador convierte un programa en este "lenguaje ensamblador" a una ristra de dígitos binarios en memoria que se corresponden, en código máquina, con las instrucciones que nosotros hemos solicitado realizar al procesador en ensamblador.

Una vez el programa está totalmente acabado (asumiendo que no tenga fallos y no sea necesario depurarlo) sólo es necesario realizar una vez el proceso de ensamblado. Por ejemplo, los programadores de un juego ensamblarán el listado del mismo, obtendrán una ristra de dígitos binarios en memoria, y la salvarán en cinta. Lo que se distribuye a los usuarios es el programa en código máquina que el Spectrum cargará en memoria y ejecutará.

El proceso de ensamblado puede ser manual: nosotros podemos utilizar una tabla de traducción instrucciones → opcodes y traducir manualmente cada instrucción en el opcode correspondiente. No obstante, lo más normal es utilizar un programa ensamblador, que automatiza este proceso por nosotros.

En este curso, programaremos nuestras rutinas o programas en lenguaje ensamblador en un fichero de texto con extensión .asm, y con un programa ensamblador cruzado lo traduciremos al código binario que entiende la CPU del Spectrum. Ese código binario puede ser ejecutado, instrucción a instrucción, por el Z80, realizando las tareas que nosotros le encomendemos en nuestro programa.

En este capítulo no vamos a ver la sintaxis e instrucciones disponibles en el ensamblador del microprocesador Z80: eso será algo que haremos capítulo a capítulo del curso. Por ahora nos debe bastar conocer que el lenguaje ensamblador es mucho más limitado en cuanto a instrucciones que BASIC, y que, a base de pequeñas piezas, debemos montar nuestro programa entero, que será sin duda mucho más rápido en cuanto a ejecución.

Como las piezas de construcción son tan pequeñas, para hacer tareas que son muy sencillas en BASIC, en ensamblador necesitaremos muchas líneas de programa, es por eso que los programas en ensamblador en general requieren más tiempo de desarrollo y se vuelven más complicados de mantener (de realizar cambios, modificaciones) y de leer conforme crecen. Debido a esto cobra especial importancia hacer un diseño en papel de los bloques del programa (y seguirlo) antes de programar una sóla línea del mismo. También se hacen especialmente importantes los comentarios que introduzcamos en nuestro código, ya que clarificarán su lectura en el futuro. El diseño es CLAVE y VITAL a la hora de programar: sólo se debe implementar lo que está diseñado previamente, y cualquier modificación de las especificaciones debe resultar en una modificación del diseño.

Así pues, resumiendo, lo que haremos a lo largo de este curso será aprender la arquitectura interna del Spectrum, su funcionamiento a nivel de CPU, y los fundamentos de su lenguaje ensamblador, con el objetivo de programar rutinas que integraremos en nuestros programas BASIC, o bien programas completos en ensamblador que serán totalmente independientes del lenguaje BASIC. 


Ejemplo: Integrar código máquina en programas BASIC
=============================================================

Supongamos que sabemos ensamblador y queremos mejorar la velocidad de un programa BASIC utilizando una rutina en código máquina. El lector se preguntará: "¿cómo podemos hacer esto?".

La integración de rutinas en código máquina dentro de programas BASIC se realiza a grandes rasgos de la siguiente forma:

Primero escribimos nuestra rutina en ensamblador, por ejemplo una rutina que realiza un borrado de la pantalla mucho más rápidamente que realizarlo en BASIC, o una rutina de impresión de Sprites o gráficos, etc.

Una vez escrito el programa o la rutina, la ensamblamos (de la manera que sea: manualmente o mediante un programa ensamblador) y obtenemos en lugar del código ASM una serie de valores numéricos que representan los códigos de instrucción en código máquina que se corresponden con nuestro listado ASM.

La siguiente figura muestra a título de ejemplo parte de una tabla de ensamblado manual, como la que utilizaban en la década de los 80 y 90 los programadores que no podían comprar un software ensamblador: 


.. figure:: tablamanual.gif
   :scale: 80 %
   :alt: Tabla de códigos ensamblador

   Tabla de códigos ensamblador



Utilizando la anterior tabla, o bien un programa ensamblador, transformamos nuestro programa ensamblador en código máquina.

Tras el proceso de ensamblado y la obtención del código máquina, nuestro programa en BASIC debe cargar esos valores en memoria (mediante LOAD "" CODE o mediante instrucciones POKE) y después saltar a la dirección donde hemos POKEADO la rutina para ejecutarla.

Veamos un ejemplo de todo esto. Supongamos el siguiente programa en BASIC, que está pensado para rellenar toda la pantalla con un patrón de píxeles determinado: 

.. code-block:: basic

    10 FOR n=16384 TO 23295
    20 POKE n, 162
    30 NEXT n

.. figure:: 1_ejemplo1.gif
   :scale: 80 %
   :alt: Patrón de pixeles del programa BASIC

   Patrón de pixeles del programa BASIC


Tras teclear y ejecutar el programa, si medimos el tiempo necesario para "pintar" toda la pantalla obtendremos que tarda aproximadamente 1 minuto y 15 segundos.

A continuación vamos a ver el mismo programa escrito en lenguaje ensamblador: 

.. code-block:: tasm 

    ; Listado 2: Rellenado de pantalla
    ORG 40000
    LD HL, 16384
    LD A, 162
    LD (HL), A
    LD DE, 16385
    LD BC, 6911
    LDIR
    RET

 Si ensamblamos este programa con un programa ensamblador y lo ejecutamos, veremos que tarda menos de 1 segundo en ejecutar la misma tarea. Es en ejemplos tan sencillos como este donde podemos ver la diferencia de velocidad entre BASIC y ASM.

Supongamos que ensamblamos a mano el listado anterior, mediante una tabla de conversión de Instrucciones ASM a Códigos de Operación (opcodes) del Z80, ensamblando manualmente (tenemos una tabla de conversión en el mismo manual del +2, por ejemplo).

Ensamblar a mano, como ya hemos dicho, consiste en escribir el programa y después traducirlo a códigos de operación consultando una tabla que nos dé el código correspondiente a cada instrucción en ensamblador.

Así pues, ensamblamos manualmente la siguiente rutina: 

.. code-block:: tasm

    LD HL, 16384
    LD A, 162
    LD (HL), A
    LD DE, 16385
    LD BC, 6911
    LDIR
    RET

Tras el ensamblado del código ensamblador obtendremos el siguiente código máquina (una rutina de 15 bytes de tamaño): ``$21, $00, $40, $3e, $a2, $77, $11, $01, $40, $01, $ff, $1a, $ed, $b0, $c9`` O, en base decimal: ``33, 0, 64, 62, 162, 119, 17, 1, 64, 1, 255, 26, 237, 176, 201``

 Como ya hemos visto en la definición de "código máquina", esta extraña ristra de bytes para nosotros incomprensible tiene un total significado para nuestro Spectrum: cuando él encuentra, por ejemplo, los bytes "62, 162", sabe que eso quiere decir "LD A, 162"; cuando encuentra el byte "201", sabe que tiene que ejecutar un "RET", y así con todas las demás instrucciones.

Un detalle: si no queremos ensamblar a mano podemos ensamblar el programa con un ensamblador como "PASMO" o "z80asm" y después obtener esos números abriendo el fichero .bin resultando con un editor hexadecimal (que no de texto).

A continuación vamos a BASIC y tecleamos el siguiente programa: 

.. code-block:: basic

    10 CLEAR 39999
    20 DATA 33, 0, 64, 62, 162, 119, 17, 1, 64, 1, 255, 26, 237, 176, 201
    30 FOR n=0 TO 14
    40 READ I
    50 POKE (40000+n), I
    60 NEXT n

 Este programa guarda a partir de la dirección 40000 los diferentes bytes del DATA (usando POKE), almacenando así nuestra rutina en memoria.

Tras esto ejecutamos un RANDOMIZE USR 40000 lo que provoca la ejecución de la rutina posicionada en la dirección 40000, que justo es la rutina que hemos ensamblado a mano y pokeado mediante el programa en BASIC.

Lo que hemos hecho en el programa BASIC es: 


* Con el CLEAR nos aseguramos de que tenemos libre la memoria desde 40000 hacia arriba (hacemos que BASIC se situe por debajo de esa memoria).
* La línea DATA contiene el código máquina de nuestra rutina.
* Con el bucle FOR hemos POKEado la rutina en memoria a partir de la dirección 40000 (desde 40000 a 40015).
* El RANDOMIZE USR 40000 salta la ejecución del Z80 a la dirección 40000, donde está nuestra rutina. Recordad que nuestra rutina acaba con un RET, que es una instrucción de retorno que finaliza la rutina y realiza una "vuelta" al BASIC.

 Siguiendo este mismo procedimiento podemos generar todas las rutinas que necesitemos y ensamblarlas, obteniendo ristras de código máquina que meteremos en DATAs y pokearemos en memoria.

Otra opción, para evitar los DATAs y los POKEs, es grabar en cinta el fichero BIN resultante del ensamblado (convertido a TAP) tras nuestro programa en BASIC, y realizar en nuestro programa un **LOAD "" CODE DIRECCION_DESTINO** de forma que carguemos todo el código binario ensamblado en memoria.

Podemos así realizar muchas rutinas en un mismo fichero ASM y ensamblarlas y cargarlas en memoria de una sola vez. Tras tenerlas en memoria, tan sólo necesitaremos saber la dirección de inicio de cada una de las rutinas para llamarlas con el **RANDOMIZE USR DIRECCION_RUTINA** correspondiente en cualquier momento de nuestro programa BASIC.

Para hacer esto, ese fichero ASM podría tener una forma como la siguiente: 

.. code-block:: tasm

    ; La rutina 1
    ORG 40000
    rutina1:
    ; Aquí la rutina 1
    RET

    ; La rutina 2
    ORG 41000
    rutina2:
    ; Aquí la rutina 2
    RET

También podemos ensamblarlas por separado y después cargarlas con varios LOAD "" CODE.

Hay que tener mucho cuidado a la hora de teclear los DATAs (y de ensamblar) si lo hacemos a mano, porque equivocarnos en un sólo número cambiaría totalmente el significado del programa y no haría lo que debería haber hecho el programa correctamente pokeado en memoria.

Un detalle más avanzado sobre ejecutar rutinas desde BASIC es el hecho de que podamos necesitar pasar parámetros a una rutina, o recibir un valor de retorno desde una rutina.

Pasar parámetros a una rutina significa indicarle a la rutina uno o más valores para que haga algo con ellos. Por ejemplo, si tenemos una rutina que borra la pantalla con un determinado patrón o color, podría ser interesante poder pasarle a la rutina el valor a escribir en memoria (el patrón). Esto se puede hacer de muchas formas: la más sencilla sería utilizar una posición libre de memoria para escribir el patrón, y que la rutina lea de ella. Por ejemplo, si cargamos nuestro código máquina en la dirección 40000 y consecutivas, podemos por ejemplo usar la dirección 50000 para escribir uno (o más) parámetros para las rutinas. Un ejemplo: 

.. code-block:: tasm

    ; Listado 3: Rellenado de pantalla
    ; recibiendo el patron como parametro.
    ORG 40000

    ; En vez de 162, ponemos en A lo que hay en la
    ; dirección de memoria 50000
    LD A, (50000)

    ; El resto del programa es igual:
    LD HL, 16384
    LD (HL), A
    LD DE, 16385
    LD BC, 6911
    LDIR
    RET

Nuestro programa en BASIC a la hora de llamar a esta rutina (una vez ensamblada y pokeada en memoria) haría: 

.. code-block:: basic

    POKE 50000, 162
    RANDOMIZE USR 40000

 Este código produciría la misma ejecución que el ejemplo anterior, porque como parámetro estamos pasando el valor 162, pero podríamos llamar de nuevo a la misma función en cualquier otro punto de nuestro programa pasando otro parámetro diferente a la misma, cambiando el valor de la dirección 50000 de la memoria. Esto rellenaría la pantalla con un patrón que deseemos, pudiendo ser éste diferente del utilizado en el anterior ejemplo, simplemente variando el valor pokeado en la dirección 50000 (el parámetro de la rutina).

En el caso de necesitar más de un parámetro, podemos usar direcciones consecutivas de memoria: en una rutina de dibujado de sprites, podemos pasar la X en la dirección 50000, la Y en la 50001, y en la 50002 y 50003 la dirección en memoria (2 bytes porque las direcciones de memoria son de 16 bits) donde tenemos el Sprite a dibujar, por ejemplo. Todo eso lo veremos con más detalle en posteriores capítulos. En este ejemplo hemos utilizado la dirección 50000, pero lo normal es utilizar direcciones concretas y reservadas dentro del propio programa ensamblado para asegurar que no hay colisión con otras rutinas que pueda haber o podamos necesitar instalar en la dirección 50000.

Además de recibir parámetros, puede sernos interesante la posibilidad de devolver a BASIC el resultado de la ejecución de nuestro programa. Por ejemplo, supongamos que realizamos una rutina en ensamblador que hace un determinado cálculo y debe devolver, tras todo el proceso, un valor. Ese valor lo queremos asignar a una variable de nuestro programa BASIC para continuar trabajando con él.

Un ejemplo: imaginemos que realizamos una rutina que calcula el factorial de un número de una manera mucho más rapida que su equivalente en BASIC. Para devolver el valor a BASIC en nuestra rutina ASM, una vez realizados los cálculos, debemos dejarlo dentro del registro BC justo antes de hacer el RET. Una vez programada la rutina y pokeada, la llamamos mediante: 

.. code-block:: basic

    LET VALOR=USR 40000

Con esto la variable de BASIC VALOR contendrá la salida de nuestra rutina (concretamente, el valor del registro BC antes de ejecutar el RET). Las rutinas sólo pueden devolver un valor (el registro BC), aunque siempre podemos (dentro de nuestra rutina BASIC) escribir valores en direcciones de memoria y leerlos después con PEEK dentro de BASIC (al igual que hacemos para pasar parámetros).

Código máquina en MICROHOBBY
================================================

Lo que hemos visto hasta ahora es que podemos programar pequeñas rutinas y llamarlas desde programas en BASIC fácilmente. Todavía no hemos aprendido nada del lenguaje en sí mismo, pero se han asentado muchos de los conceptos necesarios para entenderlo en las próximas entregas del curso.

En realidad, muchos de nosotros hemos introducido código máquina en nuestros Spectrums sin saberlo, cuando tecleabamos los listados de programa que venían en la fabulosa revista Microhobby. Muchos de los programas nos hacían introducir código máquina, aunque no lo pareciera.

Algunas veces lo hacíamos en forma de DATAs, integrados en el programa BASIC que estábamos tecleando, pero otras lo hacíamos mediante el famoso Cargador Universal de Código Máquina (CUCM).

Para que os hagáis una idea de qué era el CUCM de Microhobby, no era más que un programa en el cual tecleabamos los códigos binarios de rutinas ASM ensambladas previamente. Se tecleaba una larga línea de números en hexadecimal agrupados juntos (ver la siguiente figura), y cada 10 bytes o pares de dígitos se debía introducir un número a modo de CRC que aseguraba que los 10 dígitos (20 caracteres) anteriores habían sido introducidos correctamente. Este CRC podía no ser más que la suma de todos los valores anteriores, para asegurarse de que no habíamos tecleado incorrectamente el listado. 

.. figure:: cucm.jpg
   :scale: 80 %
   :alt: Un listado para el cargador universal de código máquina

   Un listado para el cargador universal de código máquina


Al acabar la introducción en todo el listado en el CUCM, se nos daba la opción de grabarlo. Al grabarlo indicábamos el tamaño de la rutina en bytes y la dirección donde la ibamos a alojar en memoria (en el ejemplo de la captura, la rutina se alojaría en la dirección 53000 y tenía 115 bytes de tamaño). El CUCM todo lo que hacía era un simple:


.. code-block:: basic

    SAVE "DATOS.BIN" CODE 53000, 115

Esto grababa el bloque de código máquina en cinta (justo tras nuestro programa en BASIC), de forma que el juego en algún momento cargaba esta rutina con LOAD "" CODE, y podía utilizarla mediante un RANDOMIZE USR 53000. 


PASMO: ensamblador cruzado
===================================

El lector se preguntará: "Ensamblar programas a mano es muy costoso y complejo, ¿cómo vamos a ensamblar los listados que veamos a lo largo del curso, o los que yo realice para ir practicando o para que sean mis propias rutinas o programas?".

Sencillo: lo haremos con pasmo, un programa ensamblador cruzado. Pasmo nos permitirá programar en un PC o MAC (utilizando nuestro editor de textos habitual), y después ensamblar ese fichero .asm que hemos realizado, obteniendo un fichero .BIN (o directamente un .TAP).

Los programadores "originales" en la época del Spectrum tenían que utilizar programas ensamblador nativos como MONS y GENS para todo el proceso de desarrollo. Estos programas (que corren sobre el Spectrum) implicaban teclear los programas en el teclado del Spectrum, grabarlos en cinta, ensamblar y grabar el resultado en cinta, etc. Actualmente es mucho más cómodo usar ensambladores cruzados como los que usaremos en nuestro curso.

Nuestra opción preferente como ensamblador cruzado es Pasmo. Pasmo es un ensamblador cruzado, opensource y multiplataforma. Con Pasmo podremos programar en nuestro PC, grabar un fichero ASM y ensamblarlo cómodamente, sin cintas de por medio. Tras todo el proceso de desarrollo, podremos llevar el programa resultante a una cinta (o disco) y ejecutarlo por lo tanto en un Spectrum real, pero lo que es el proceso de desarrollo se realiza en un PC, con toda la comodidad que eso conlleva.

Pasmo en su versión para Windows/DOS es un simple ejecutable (pasmo.exe) acompañado de ficheros README de información. Podemos mover el fichero pasmo.exe a cualquier directorio que esté en el PATH o directamente ensamblar programas (siempre desde la línea de comandos o CMD, no directamente mediante "doble click" al ejecutable) en el directorio en el que lo tengamos copiado.

La versión para Linux viene en formato código fuente (y se compila con un simple make) y su binario "pasmo" lo podemos copiar, por ejemplo, en /usr/local/bin.



Generando código binario para programas BASIC
--------------------------------------------------
Iremos viendo el uso de pasmo conforme lo vayamos utilizando, pero a título de ejemplo, veamos cómo se ensamblaría el programa que vimos en el apartado de integración de BASIC y ASM. Primero tecleamos el programa en un fichero de texto y después pasmo para ensamblarlo::

     pasmo ejemplo1.asm ejemplo1.bin

 Como resultado del proceso de ensamblado obtendremos un fichero .bin que contiene el código máquina que podremos utilizar directamente en los DATAs de nuestro programa en BASIC.

El fichero .bin es binario, por lo que para obtener los valores numéricos que introducir en los datas debemos utilizar un editor hexadecimal o alguna utilidad como "hexdump" de Linux::

    $ hexdump -C ejemplo1.bin
    00000000  21 00 40 3e a2 77 11 01 40 01 ff 1a ed b0 c9

Ahí tenemos los datos listos para convertirlos a decimal y pasarlos a sentencias DATA. Si el código es largo y no queremos teclear en DATAs la rutina, podemos convertir el BIN en un fichero TAP ensamblando el programa mediante::

    pasmo --tap ejemplo1.asm ejemplo1.tap

Este fichero tap contendrá ahora un tap con el código binario compilado tal y como si lo hubieras introducido en memoria y grabado con SAVE "" CODE, para ser cargado posteriormente en nuestro programa BASIC con LOAD "" CODE.

Esta segunda opción (LOAD "" CODE) es la más cómoda, pues nos evita el pokeado de valores en memoria, pero implica ubicar el bloque de datos a cargar con LOAD "" CODE a continuación del programa en BASIC dentro del fichero .tap.

Para realizar esta concatenación escribimos las rutinas en un fichero .ASM y las compilamos con "pasmo –tap fichero.asm bloque_cm.tap". Después, escribimos nuestro programa en BASIC y lo salvamos en cinta, obteniendo otro fichero tap (programa_basic.tap).

Tras esto tenemos que crear un TAP o un TZX que contenga primero el bloque BASIC y después el bloque de código máquina, de forma que el bloque BASIC podrá cargar el bloque de código máquina con un ``LOAD "" CODE DIRECCION, TAMANYO_BLOQUE_CM``.

Podemos realizar esto con herramientas de gestión de ficheros TAP/TZX o, sin necesidad de utilizar emuladores o herramientas adicionales, mediante concatenación de ficheros:

* Linux: ``cat programa_basic.tap bloque_cm.tap > programa_completo.tap``
* Windows: ``copy /b programa_basic.tap +bloque_cm.tap programa_completo.tap``


Generando un binario desde un programa íntegramente en ensamblador
---------------------------------------------------------------------


Si estamos realizando un programa completo en ensamblador, sin ninguna parte en BASIC, deberemos compilar el programa mediante "pasmo –tapbas fichero.asm fichero.tap". La opción –tapbas añade una cabecera BASIC que carga el bloque código máquina en la dirección indicada por la sentencia ORG del programa en ensamblador (por ejemplo, 40000).

El fichero resultante del ensamblado será un TAP sin autoejecución listo para cargar en el Spectrum y que deberemos lanzar con un RANDOMIZE USR 40000.

Finalmente, si agregamos una sentencia END a nuestro programa y le agregamos la dirección de inicio (ORG) del mismo, en ese caso "pasmo –tapbas" agregará el RANDOMIZE USR correspondiente al listado BASIC y el programa se autoejecutará al ser cargado. 

.. code-block:: tasm

    ; Pruebas de ensamblador para z80-asm
    ; Santiago Romero aka NoP/Compiler
    ORG 40000
    LD HL, 16384
    LD A, 162
    LD (HL), A
    LD DE, 16385
    LD BC, 6911
    LDIR
    RET
    END 40000            ; Pasmo añade RANDOMIZE USR 40000

El resultado del ensamblado de este ejemplo con –tapbas será directamente ejecutable en un Spectrum con un simple LOAD "". 

En resumen
================

En esta entrega hemos definido las bases del curso de ensamblador de Z80, comenzando por las limitaciones de BASIC y la necesidad de conocer un lenguaje más potente y rápido. Hemos visto qué aspecto tiene el código en ensamblador (aunque todavía no conozcamos la sintaxis) y, muy importante, hemos visto cómo se integra este código en ensamblador dentro de programas en BASIC.

Por último, hemos conocido una utilidad (pasmo) que nos permitirá, a lo largo del curso, ensamblar todos los programas que realicemos, así como probarlos en un emulador o integrar rutinas en nuestros programas BASIC. 