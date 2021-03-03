Arquitectura y funcionamiento del Spectrum
==============================================

La Arquitectura del Spectrum
-----------------------------------

Antes de comenzar a programar en lenguaje ensamblador para Spectrum necesitamos conocer su arquitectura: ¿qué hay dentro de nuestro pequeño ordenador y cómo funciona internamente? ¿Cómo procesa las instrucciones código máquina?

En BASIC muchas veces podemos olvidarnos de los detalles a nivel de hardware (precisamente ese es el objetivo de un lenguaje de Alto Nivel como es BASIC), pero en ensamblador no: al escribir los programas en un lenguaje con traducción directa al código máquina es imprescindible conocer cómo funciona internamente el procesador al cual le estamos dando instrucciones.

En este capítulo veremos una visión simplificada de la arquitectura hardware del Spectrum pero que en el fondo es todo lo que necesitaremos para el desarrollo de la mayoría de programas. Bajar hasta el nivel de la electrónica en sí sería una labor para otro tipo de cursos y tendría su principal aplicación en el desarrollo de hardware más que de software.

Comencemos con un esquema de cómo es internamente nuestro Spectrum a nivel de hardware, y después comentaremos uno a uno los elementos que lo componen: 

.. figure:: esquema_zx.png
   :scale: 80 %
   :alt: Esquema del ZX Spectrum

   Arquitectura del Spectrum


En un vistazo general, podemos ver que el microprocesador Z80 se conecta mediante los puertos de entrada/salida de la CPU a los periféricos externos (teclado, cassette y altavoz de audio), pudiendo leer el estado de los mismos (leer del teclado, leer del cassette) y escribir en ellos (escribir en el altavoz para reproducir sonido, escribir en el cassette) por medio de estas conexiones conocidas como “I/O Ports”.

Al mismo tiempo, los Buses de Datos y de Direcciones conectan al microprocesador con la memoria. Esta conexión es la que permite que el Z80 pueda leer y escribir en cualquier posición de la RAM, y leer datos de la ROM (que, juntas, conforman la totalidad de la memoria disponible).

Cuando encendemos el Spectrum, el microprocesador Z80 se dedicada a leer valores de la memoria, decodificar a qué instrucción se corresponde el valor que acaba de leer, y ejecutarlo, continuando el proceso con la siguiente posición de memoria. Así pues, empezando por la posición 0000, el Spectrum comienza a leer instrucciones y a ejecutarlas, una a una.

Al comienzo de la memoria, desde la posición 0 hasta la 16384 (16KB) tenemos mapeada la ROM (Read Only Memory o memoria de sólo lectura) del Spectrum, que contiene instrucciones de programa preprogramadas y que no podemos modificar: contiene las funciones básicas del “sistema operativo” del Spectrum, incluyendo el intérprete de BASIC.

Después de estos primeros 16KB de memoria (la ROM) viene el resto de la memoria disponible: la memoria RAM (Random Access Memory o memoria de acceso aleatorio). Esta es la parte de la memoria en la que nuestros programas pueden trabajar: en ella alojaremos el código del programa, las variables del mismo, etc.

Por otro lado, el microprocesador Z80 tiene una serie de registros internos con los que trabaja y que son los que manipula y utiliza para ejecutar las instrucciones almacenadas en la memoria.

Por último, el puerto de expansión del Spectrum permite conectar nuevos periféricos (como el adaptador de Joystick Kempston o el Interface 1 ó 2) directamente a las patillas de la CPU, ampliando las funcionalidades del ordenador.

Veamos más detalladamente los diferentes componentes de la arquitectura del Spectrum, y cómo funcionan.


El microprocesador Z80
-----------------------

Como podemos distinguir en el esquema, el cerebro de nuestro Spectrum es un microprocesador Zilog Z80A a 3,54Mhz. Un microprocesador es un circuito integrado que consta (principalmente) de registros, microcódigo, puertos de entrada/salida, un bus de datos y uno de direcciones.

.. figure:: z80.jpg
   :scale: 80 %
   :alt: El microprocesador Zilog Z80

   El microprocesador Zilog Z80

Los registros son contenedores de valores numéricos que residen dentro de la misma CPU. En el caso del Z80, tiene 2 juegos de registros (los registros en uso, y los registros alternativos o shadow).

Cada uno de los 2 juegos de registro está formado por las mismas “piezas”: Tenemos por un lado registros de un byte como **A**, **F**, **B**, **C**, **D**, **E**, **H**, **L**, **I** y **R**, y registros de dos bytes como **IX**, **IY**, **SP** y **PC**. Los registros de un byte pueden contener valores de 8 bits, es decir, de 0 a 255, y los de 2 bytes pueden contener valores de 16 bits (0-65535).

Algunos de los registros que hemos nombrado pueden agruparse para formar registros de mayor tamaño y así poder realizar operaciones que requieran valores mayores que los que se pueden representar con 8 bits. Por ejemplo, **H** y **L** pueden formar juntos el registro **HL** con el que realizar operaciones de 16 bits concretas.

Veremos los registros en detalle en el próximo capítulo (así como el segundo juego de registros disponible), pero podemos hacernos a la idea de que los registros son simples variables de 8 ó 16 bits que utilizaremos en nuestros programas en ensamblador. Así, podremos cargar un valor en un registro (**LD A, 25**), sumar un registro con otro (**ADD A, B**), activar o desactivar determinados bits de un registro (**SET 7, A**), etc. 

.. figure:: debugger1.png
   :scale: 80 %
   :alt: Depurador del emulador FUSE

   Depurador del emulador FUSE


El juego de registros es todo lo que tenemos (aparte de la memoria) para realizar operaciones en nuestro programa: siempre que estemos operando con datos o utilizando variables, tendrá que ser por fuerza un registro, o una posición de memoria que usemos como variable. Por ejemplo, podemos escribir el siguiente programa en ensamblador, que sumaría dos números: 

.. code-block:: tasm

    LD A, 10
    LD B, 20
    ADD A, B

 El anterior programa, una vez ensamblado y ejecutado en un Z80, vendría a decir:

* Carga en el registro A el valor “10”.
* Carga en el registro B el valor “20”.
* Suma el valor del registro A con el del registro B y deja el resultado en el registro A (A=A+B).

Tras ejecutar el anterior programa en un Z80, el contenido del registro A sería 30 (10+20).

Cuando tratemos las diferentes instrucciones del Z80 veremos en más detalle los registros, su tamaño, cómo se agrupan, y de qué forma podemos usarlos para operar entre ellos y realizar nuestras rutinas o programas.

Finalmente, existe un registro especial del procesador llamado PC (Program Counter, o Contador de Programa). Este registro es de 16 bits (puede contener un valor entre 0 y 65535), y su utilidad es la de apuntar a la dirección de memoria de la siguiente instrucción a ejecutar. Así, cuando arrancamos nuestro Spectrum, el registro PC vale $0000, con lo que lo primero que se ejecuta en el Spectrum es el código que hay en $0000. Una vez leído y ejecutado ese primer código de instrucción, se incrementa PC para apuntar al siguiente, y así continuadamente.

Los programas se ejecutan linealmente mediante un ciclo basado en: Leer instrucción en la dirección de memoria apuntada por PC, incrementar registro PC, ejecutar instrucción. Posteriormente veremos más acerca de PC.

Ya hemos visto qué son los registros del microprocesador. Ahora bien, en el ejemplo anterior, ¿cómo sabe el microprocesador qué tiene que hacer cuando se encuentra un comando “LD” o “ADD”? Esto es tarea del microcódigo. El microcódigo del microprocesador es una definición de qué tiene que hacer el microprocesador ante cada una de las posibles órdenes que nosotros le demos.

Por ejemplo, cuando el microprocesador está ejecutando nuestro anterior programa y lee los valores numéricos correspondientes a “LD A, 10”, el Z80 utiliza el microcódigo encargado de mover el valor 10 al registro A. Este microcódigo no es más que una secuencia de señales hardware y cambios de estados electrónicos cuyo resultado será, exactamente, activar y desactivar BITs en el registro A (que no es más que una serie de 8 biestables electrónicos que pueden estar a 0 voltios o a 5 voltios cada uno de ellos, representando el estado de los 8 bits del registro A). Lo mismo ocurrirá cuando se lea la instrucción “LD B, 20”, sólo que se ejecutará otra porción de microcódigo que lo que hará será modificar el registro B.

Este microcódigo está dentro del microprocesador porque sus diseñadores implementaron todas y cada una de las operaciones que puede hacer el Z80. Cuando pedimos meter un valor en un registro, leer el valor de un registro, sumar un registro con otro, escribir el valor de un registro en una dirección de memoria, saltar a otra parte del programa, etc, para cada una de esas situaciones, hay un microcódigo (implementado mediante hardware) que realiza esa tarea.

Nosotros no tendremos que preocuparnos pués de cómo hace el Z80 las cosas internamente a nivel de microcódigo, aunque es bueno que conozcáis cómo llega el Spectrum a ejecutar nuestros comandos: gracias al microcódigo. 