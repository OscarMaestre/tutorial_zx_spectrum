Gráficos (y III): Sprites y Gráficos en baja resolución (bloques)
================================================================================



En este capítulo crearemos rutinas específica de impresión de sprites de 8×8 píxeles en posiciones exáctas de carácter (gráficos de bloques) y la extenderemos a la impresión de sprites de 16×16 píxeles (2×2 bloques). Además de estas rutinas de tamaños específicos, analizaremos una rutina más genérica que permita imprimir sprites de tamaños múltiples del anterior (16×16, 24×16, etc).

Imprimir en posiciones exactas de carácter (de 0 a 31 para la coordenada X, y de 0 a 23 para la coordenada Y), coincidiendo con las posiciones posibles de la rejilla de 32×24 en pantalla es lo que se conoce como “gráficos en baja resolución”. Los gráficos, aunque sean muy detallados, se mueven “carácter a carácter”.

El capítulo hará uso intensivo de los algoritmos de cálculo de direcciones de memoria a partir de coordenadas y del movimiento relativo descritos en 2 anteriores capítulos, aunque las rutinas mostradas a continuación podrían ser directamente utilizadas incluso sin conocimientos sobre la organización de la videomemoria del Spectrum.

Estudiaremos también los métodos de impresión sobre pantalla: transferencia directa, operaciones lógicas y uso de máscaras, y la generación de los datos gráficos y de atributos a partir de la imagen formada en un editor de sprites. 

Teoría sobre el trazado de sprites
--------------------------------------------------------------------------------



Comencemos con las definiciones básicas de la terminología que se usará en este capítulo.


Sprite: Se utiliza el término anglosajón sprite (traducido del inglés: “duendecillo”) para designar en un juego o programa a cualquier gráfico que tenga movimiento. En el caso del Spectrum, que no tiene como otros sistemas hardware dedicado a la impresión de Sprites, aplicamos el término a cualquier mapa de bits (del inglés bitmap) que podamos utilizar en nuestros programas: el gráfico del personaje protagonista, los de los enemigos, los gráficos de cualquier item o incluso las propias fuentes de texto de los marcadores. 



.. figure:: gfx3_sprite.png
   :scale: 50%
   :align: center
   :alt: Sprite

   Sprite


Editor de Sprites: Los sprites se diseñan en editores de sprites, que son aplicaciones diseñadas para crear Sprites teniendo en cuenta la máquina destino para la que se crean. Por ejemplo, un editor de Sprites para Spectrum tomará en cuenta, a la hora de aplicar colores, el sistema de tinta/papel en bloques de 8×8 píxeles y no nos permitirá dibujar colores saltándonos dicha limitación que después existirá de forma efectiva en el hardware destino. 



.. figure:: gfx3_sevenup.png
   :scale: 50%
   :align: center
   :alt: Gráficos en SevenUP

   Gráficos en SevenUP

Estos programas gráficos tratan los sprites como pequeños rectángulos (con o sin zonas transparentes en ellos) del ancho y alto deseado y se convierten en mapas de bits (una matriz de píxeles activos o no activos agrupados) que se almacenan en los programas como simples ristras de bytes, preparados para ser volcados en la pantalla con rutinas de impresión de sprites.



.. figure:: gfx3_sprite_bitmap.png
   :scale: 50%
   :align: center
   :alt: Sprite Bitmap

   Sprite Bitmap



Rutinas de impresión de Sprites: son rutinas que reciben como parámetro la dirección en memoria del Sprite y sus Atributos y las coordenadas (x,y) destino, y vuelcan esta información gráfica en la pantalla.


Sprite Set: Normalmente todos los Sprites de un juego se agrupan en un “sprite set” (o “tile set”), que es una imagen rectangular o un array lineal que almacena todos los datos gráficos del juego de forma que la rutina de impresión de Sprites pueda volcar uno de ellos mediante unas coordenadas origen y un ancho y alto (caso del tileset rectangular) o mediante un identificador dentro del array de sprites (caso del tileset lineal).

El sistema de sprites en formato rectangular suele ser utilizado en sistemas más potentes que el Spectrum, permitiendo además sprites de diferentes tamaños en el mismo tileset. Las rutinas que imprimen estos sprites a lo largo del juego requieren como parámetros, además de la posición (x,y) de destino, una posición (x,y) de origen y un ancho y alto para “extraer” cada sprite de su “pantalla origen” y volcarlo a la pantalla destino.



.. figure:: pacman_simonowen.png
   :scale: 50%
   :align: center
   :alt: Sprites de Pacman

   Sprites de Pacman


En el caso del Spectrum, nos interesa mucho más el sistema de almacenamiento lineal dentro de un “vector” de datos, ya que normalmente agruparemos todos los sprites de un mismo tamaño en un mismo array. Podremos disponer de diferentes arrays para elementos de diferentes tamaños. Cuando queramos hacer referencia a uno de los sprites de dicho array, lo haremos con un identificador numérico (0-N) que indicará el número de sprite que queremos dibujar comenzando desde arriba y designando al primero como 0. 



.. figure:: gfx3_tilesetsk.png
   :scale: 50%
   :align: center
   :alt: Tileset

   Tileset



En un juego donde todos los sprites son de 16×16 y los fondos están formados por sprites o tiles de 8×8, se podría tener un “array” para los sprites, otro para los fondos, y otro para las fuentes de texto. Durante el desarrollo del bucle del programa llamaremos a la rutina de impresión de sprites pasando como parámetro el array de sprites, el ancho y alto del sprite, y el identificador del sprite que queremos dibujar.


Frame (fotograma): El “sprite set” no sólo suele alojar los diferentes gráficos de cada personaje o enemigo de un juego, sino que además se suelen alojar todos los frames (fotogramas) de animación de cada personaje. En sistemas más modernos se suele tener un frameset (un array de frames) por cada personaje, y cada objeto del juego tiene asociado su frameset y su estado actual de animación y es capaz de dibujar el frame que le corresponde.
En el Spectrum, por limitaciones de memoria y código, lo normal es tener todo en un mismo spriteset, y tener almacenados los identificadores de animación de un personaje en lugar de su frameset. Así, sabremos que nuestro personaje andando hacia la derecha tiene una animación que consta de los frames (por ejemplo) 10, 11 y 12 dentro del spriteset.


Tiles: Algunos bitmaps, en lugar de ser llamados “sprites”, reciben el nombre de tiles (“bloques”). Normalmente esto sucede con bitmaps que no van a tener movimiento, que se dibujan en posiciones exáctas de carácter, y/o que no tienen transparencia. Un ejemplo de tiles son los “bloques” que forman los escenarios y fondos de las pantallas cuando son utilizados para componer un mapa de juego en base a la repetición de los mismos. Los tiles pueden ser impresos con las mismas rutinas de impresión de Sprites (puesto que son bitmaps), aunque normalmente se diseñan rutinas específicas para trazar este tipo de bitmaps aprovechando sus características (no móviles, posición de carácter, no transparencia), con lo que dichas rutinas se pueden optimizar. Como veremos en el próximo capítulo, los tiles se utilizan normalmente para componer el área de juego mediante un tilemap (mapa de tiles): 



.. figure:: gfx3_tilemap.png
   :scale: 50%
   :align: center
   :alt: Tilemap

   Tilemap


Máscaras de Sprites: Finalmente, cabe hablar de las máscaras de sprites, que son bitmaps que contienen un contorno del sprite de forma que se define qué parte del Sprite original debe sobreescribir el fondo y qué parte del mismo debe de ser transparente. 



.. figure:: gfx3_masks.png
   :scale: 50%
   :align: center
   :alt: Máscaras

   Máscaras


Las máscaras son necesarias para saber qué partes del sprite son transparentes: sin ellas habría que testear el estado de cada bit para saber si hay que “dibujar” ese pixel del sprite o no. Gracias a la máscara, basta un AND entre la máscara y el fondo y un OR del sprite para dibujar de una sóla vez 8 píxeles sin realizar testeos individuales de bits.


Diseño de una rutina de impresión de sprites
--------------------------------------------------------------------------------



En microordenadores como el Spectrum existe un vínculo especial entre los “programadores” y los “diseñadores gráficos”, ya que estos últimos deben diseñar los sprites teniendo en cuenta las limitaciones del Spectrum y a veces hacerlo tal y como los programadores los necesitan para su rutina de impresión de Sprites o para salvar las limitaciones de color del Spectrum o evitar colisiones de atributos entre personajes y fondos.


El diseño gráfico del Sprite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



El diseñador gráfico y el programador deben decidir el tamaño y características de los Sprites y el “formato para el sprite origen” a la hora de exportar los bitmaps como “datos binarios” para su volcado en pantalla.

A la hora de crear una rutina de impresión de sprites tenemos que tener en cuenta el formato del Sprite de Origen. Casi se podría decir que más bien, la rutina de impresión de sprites debemos escribirla o adaptarla al formato de sprites que vayamos a utilizar en el juego.

Dicho formato puede ser:


* Sprite con atributos de color (multicolor) o sin atributos de color (monocolor).
* Si el sprite tiene atributos de color, los atributos pueden ir:

      * En un array de atributos aparte del array de datos gráficos.

      * En el mismo array de datos gráficos, pero detrás del último de los sprites (linealmente, igual que los sprites), como: sprite0,sprite1,atributos0,atributos1.

      * En el mismo array de datos gráficos, pero el atributo de un sprite va detrás de dicho sprite en el vector, intercalado: sprite0,atributos0,sprite1,atributos1.
* Sprite que altere o no altere el fondo:

    * Si no debe alterarlo, se tiene que decidir si será mediante impresión por operación lógica o si será mediante máscaras (y dibujar y almacenar estas).


Además, hay que tener las herramientas para el dibujado y la conversión de los bitmaps o spritesets en código, en el formato que hayamos decidido. Más adelante en el capítulo profundizaremos en ambos temas: la organización en memoria del Sprite (o del Spriteset completo) y las herramientas de dibujo y conversión.


La creación de la rutina de impresión
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





Dadas las limitaciones en velocidad de nuestro querido procesador Z80A, el realizar una rutina de impresión de sprites en alta resolución rápida es una tarea de complejidad media/alta que puede marcar la diferencia entre un juego bueno y un juego malo, especialmente conforme aumenta el número de sprites en pantalla y por tanto, el parpadeo de los mismos si la rutina no es suficientemente buena.

La complejidad de las rutinas que veremos concretamente en este capítulo será de un nivel más asequible puesto que vamos a trabajar con posiciones de carácter en baja resolución y además crearemos varias rutinas específicas y una genérica.

Para crear estas rutinas necesitamos conocer la teoría relacionada con:


* El cálculo de posición en memoria de las coordenadas (c,f) en las que vamos a dibujar el Sprite.
* El dibujado de cada scanline del sprite en pantalla, ya sea con LD/ldir o con operaciones lógicas tipo OR/XOR.
* El avance a través del sprite para acceder a otros scanlines del mismo.
* El avance diferencial en pantalla para movernos hacia la derecha (por cada bloque de anchura del sprite), y hacia abajo (por cada scanline de cada bloque y por cada bloque de altura del sprite).
* El cálculo de posición en memoria de atributos del bloque (0,0) del sprite.
* El avance diferencial en la zona de atributos para imprimir los atributos de los sprites de más de 1×1 bloques.


Gracias a los 2 últimos capítulos del curso y a nuestros conocimientos en ensamblador, ya tenemos los mecanismos para dar forma a la rutina completa.

Diseñaremos rutinas de impresión de sprites en baja resolución de 1×1 bloques (8×8 píxeles), 2×2 bloques (16×16 píxeles) y NxM bloques. Las 2 primeras rutinas, específicas para un tamaño concreto, serán más óptimas y eficientes que la última, que tendrá que adecuarse a cualquier tamaño de sprite y por lo tanto no podrá realizar optimizaciones basadas en el conocimiento previo de ciertos datos.

Por ejemplo, cuando sea necesario multiplicar algún registro por el valor del ancho del sprite, en el caso de la rutina de 1×1 no será necesario multiplicar y en el caso de la rutina de 2×2 podremos hacer uso de 1 desplazamiento a izquierda, pero la rutina de propósito general tendrá que realizar la multiplicación por medio de un bucle de sumas. Así, imprimir un sprite de 2×2 con su rutina específica será mucho más rápido que imprimir el mismo sprite con la genérica.

Aunque trataremos de optimizar las rutinas en la medida de lo posible, se va a intentar no realizar optimizaciones que hagan la rutina ilegible para el lector. Las rutinas genéricas que veremos hoy serán rápidas pero siempre podrán optimizarse más mediante trucos y técnicas al alcance de los programadores con más experiencia. Es labor del programador avanzado el adaptar estas rutinas a cada juego para optimizarlas al máximo en la medida de lo posible.

En este sentido, en alguna de las rutinas utilizaremos variables en memoria para alojar datos de entrada o datos temporales o intermedios. Aunque acceder a la memoria es “lenta” comparada con tener los datos guardados en registros, cuando comenzamos a manejar muchos parámetros de entrada (y de trabajo) en una rutina y además hay que realizar cálculos con ellos, es habitual que agotemos los registros disponibles, más todavía teniendo en cuenta la necesidad de realizar dichos cálculos. En muchas ocasiones se acaba realizando uso de la pila con continuos PUSHes y POPs destinados a guardar valores y recuperarlos posteriormente a realizar los cálculos o en ciertos puntos de la rutina.

Las instrucciones PUSH y POP toman 11 y 10 t-estados respectivamente, mientras que escribir o leer un valor de 8 bits en memoria (ld (NN), a y ld a, (NN)) requiere 13 t-estados y escribir o leer un valor de 16 bits toma 20 t-estados ld (NN), rr y ld rr, (NN)) con la excepción de ld (NN), hl que cuesta 16 t-estados. 


+--------------------+---------------------+
| Instrucción        | Tiempo en t-estados |
+====================+=====================+
| push rr            | 11                  |
+--------------------+---------------------+
| push ix o push iy  | 16                  |
+--------------------+---------------------+
| pop rr             | 10                  |
+--------------------+---------------------+
| pop ix o pop iy    | 14                  |
+--------------------+---------------------+
| ld (NN), a         | 13                  |
+--------------------+---------------------+
| ld a, (NN)         | 13                  |
+--------------------+---------------------+
| ld rr, (NN)        | 20                  |
+--------------------+---------------------+
| ld (NN), rr        | 20                  |
+--------------------+---------------------+
| ld (NN), hl        | 16                  |
+--------------------+---------------------+

Aunque es una diferencia apreciable, no siempre podemos obtener una “linealidad” de uso de la pila que requiera un POP por cada PUSH, por lo que en ocasiones se hace realmente cómodo y útil el aprovechar variables de memoria para diseñar las rutinas.

En nuestro caso utilizaremos algunas variables de memoria para facilitar la lectura de las rutinas: serán más sencillas de seguir y más intuitivas a costa de algunos ciclos de reloj. No deja de ser cierto también que los programadores en ocasiones nos obsesionamos por utilizar sólo registros y acabamos realizando combinaciones de intercambios de valores en registros y PUSHes/POPs que acaban teniendo más coste que la utilización de variables de memoria.

El programador profesional tendrá que adaptar cada rutina a cada caso específico de su programa y en este proceso de optimización podrá (o no) sustituir dichas variables de memoria por combinaciones de código que eviten su uso, aunque no siempre es posible dado el reducido juego de registros del Z80A.

Finalmente, recordar que las rutinas que veremos en este capítulo pueden ser ubicadas en memoria y llamadas desde BASIC. Una vez ensambladas y POKEadas en memoria, podemos hacer uso de ellas utilizando POKE para establecer los parámetros de llamada y RANDOMIZE USR DIR_RUTINA para ejecutarlas. A lo largo de la vida de revistas como Microhobby se publicaron varios paquetes de rutinas de gestión de Sprites en ensamblador que utilizan este método y que estaban pensadas para ser utilizadas tanto desde código máquina como desde BASIC.


Organización de los sprites en memoria
--------------------------------------------------------------------------------



Como ya hemos visto, una vez diseñados los diferentes sprites de nuestro juego hay que agruparlos en un formato que después, convertidos a datos binarios, pueda interpretar nuestra rutina de impresión.

Hay 4 decisiones principales que tomar al respecto:


* Formato de organización del tileset (lineal o en forma de matriz/imagen).
* Formato de almacenamiento de cada tile (por bloques, por scanlines).
* Formato de almacenamiento de los atributos (después de los sprites, intercalados con ellos).
* Formato de almacenamiento de las máscaras de los sprites si las hubiera.


El formato de organización del tileset no debería requerir mucho tiempo de decisión: la organización del tileset en formato lineal es mucho más eficiente para las rutinas de impresión de sprites que el almacenamiento en una “imagen” rectangular. Teniendo todos los sprites (o tiles) en un único vector, podemos hacer referencia a cualquier bloque, tile, sprite o cuadro de animación mediante un identificador numérico.

De esta forma, el “bloque 0” puede ser un bloque vacío, el bloque “1” el primer fotograma de animación de nuestro personaje, etc.

Donde sí debemos tomar decisiones importantes directamente relacionadas con el diseño de la rutina de impresión de Sprites es en la organización en memoria de los datos gráficos del sprite y sus atributos (y la máscara si la hubiera). El formato de almacenamiento de los tiles, los atributos y los datos de máscara definen la exportación de los datos desde el editor de Sprites y cómo debe de trabajar la rutina de impresión.

Veamos con un ejemplo práctico las distintas opciones de que disponemos. Para ello vamos a definir un ejemplo basado en 2 sprites de 16×8 pixeles (2 bloques de ancho y 1 de alto, para simplificar). Marcaremos cada scanline de cada bloque con una letra que representa el valor de 8 bits con el estado de los 8 píxeles, de forma que podamos estudiar las posibilidades existentes.

Así, los 16 píxeles de la línea superior del sprite (2 bytes), los vamos a identificar como “A1” y “B1”. Los siguientes 16 píxeles (scanline 2 del sprite y de cada uno de los 2 bloques), serán los bytes “C1” y “D1”, y así sucesivamente::

    Datos gráficos Sprite 1:
    | A1 | B1 |
    | C1 | D1 |
    | E1 | F1 |
    | G1 | H1 |
    | I1 | J1 |
    | K1 | L1 |
    | M1 | N1 |
    | O1 | P1 |

    Atributos Sprite 1:
    | S1_Attr1 | S1_Attr2 |

Y::

    Datos gráficos Sprite 2:
    | A2 | B2 |
    | C2 | D2 |
    | E2 | F2 |
    | G2 | H2 |
    | I2 | J2 |
    | K2 | L2 |
    | M2 | N2 |
    | O2 | P2 |

    Atributos Sprite 1:
    | S2_Attr1 | S2_Attr2 |

Al organizar los datos gráficos y de atributos en disco, podemos hacerlo de 2 formas:


Utilizando 2 arrays: uno con los datos gráficos y otro con los atributos, organizando la información horizontal por scanlines del sprite. Todos los datos gráficos o de atributo de un mismo sprite son consecutivos en memoria y el “salto” se hace al acabar cada scanline completo del sprite (no de cada bloque). La rutina de impresión recibe como parámetro la dirección de inicio de ambas tablas y traza primero los gráficos y después los atributos::

    Tabla_Sprites:
        DB A1, B1, C1, D1, E1, F1, G1, H1, I1, J1, K1
        DB L1, M1, N1, O1, P1, A2, B2, C2, D2, E2, F2
        DB G2, H2, I2, J2, K2, L2, M2, N2, O2, P2

    Tabla_Atributos:
        DB S1_Attr1, S1_Attr2, S2_Attr1, S2_Attr2


Utilizando un único array: Se intercalan los atributos dentro del array de gráficos, detrás de cada Sprite. La rutina de impresión calculará en el array el inicio del sprite a dibujar y encontrará todos los datos gráficos de dicho sprite seguidos a partir de este punto. Al acabar de trazar los datos gráficos, nos encontramos directamente en el vector con los datos de atributo del sprite que estamos tratando::

    Tabla_Sprites:
        DB A1, B1, C1, D1, E1, F1, G1, H1, I1, J1, K1
        DB L1, M1, N1, O1, P1, S1_Attr1, S1_Attr2, A2
        DB B2, C2, D2, E2, F2, G2, H2, I2, J2, K2, L2
        DB M2, N2, O2, P2, S2_Attr1, S2_Attr2

Finalmente, no debemos olvidarnos de que si utilizamos máscaras de sprite también deberemos incluirlas en nuestro “array de datos” (o sprite set). El dónde ubicar cada scanline de la máscara depende, de nuevo, de nuestra rutina de impresión. Una primera aproximación sería ubicar cada byte de máscara antes o después de cada dato del sprite, para que podamos realizar las pertinentes operaciones lógicas entre la máscara, el fondo y el sprite.

Si denominamos “XX” a los datos de la máscara del sprite 1 y “YY” a los datos de máscara del sprite 2, nuestra tabla de datos en memoria quedaría de la siguiente forma::

    ; Formato: Una única tabla:
    Tabla_Sprites:
        DB XX, A1, XX, B1, XX, C1, XX, D1, XX, E1, XX, F1, XX, G1
        DB XX, H1, XX, I1, XX, J1, XX, K1, XX, L1, XX, M1, XX, N1
        DB XX, O1, XX, P1, S1_Attr1, S1_Attr2
        DB YY, A2, YY, B2, YY, C2, YY, D2, YY, E2, YY, F2, YY, G2
        DB YY, H2, YY, I2, YY, J2, YY, K2, YY, L2, YY, M2, YY, N2
        DB YY, O2, YY, P2, S2_Attr1, S2_Attr2

    ; Formato: Dos tablas:
    Tabla_Sprites:
        DB XX, A1, XX, B1, XX, C1, XX, D1, XX, E1, XX, F1, XX, G1
        DB XX, H1, XX, I1, XX, J1, XX, K1, XX, L1, XX, M1, XX, N1
        DB XX, O1, XX, P1, YY, A2, YY, B2, YY, C2, YY, D2, YY, E2
        DB YY, F2, YY, G2, YY, H2, YY, I2, YY, J2, YY, K2, YY, L2
        DB YY, M2, YY, N2, YY, O2, YY, P2

    Tabla_Atributos:
        DB S1_Attr1, S1_Attr2, S2_Attr1, S2_Attr2


Para las rutinas que crearemos como ejemplo utilizaremos el formato lineal horizontal mediante 2 tablas, una con los gráficos y otra con los atributos de dichos gráficos. En las rutinas con máscara, intercalaremos los datos de máscara antes de cada dato del sprite, como acabamos de ver. Es el formato más sencillo para la generación de los gráficos y para los cálculos en las rutinas, y por tanto el elegido para mostrar rutinas comprensibles por el lector.

Sería posible también almacenar la información del sprite por columnas (formato lineal vertical), lo cual requeriría rutinas diferentes de las que vamos a ver en este capítulo.

A continuación hablaremos sobre el editor de Sprites SevenuP y veremos de una forma gráfica el formato de organización lineal-horizontal de datos en memoria, y cómo un gráfico de ejemplo se traduce de forma efectiva en un array de datos con el formato deseado. 


Conversion de datos graficos a códigos dibujables
--------------------------------------------------------------------------------



Para diseñar los sprites de nuestro juego necesitaremos utilizar un editor de Sprites. Existen editores de sprites nativos en el Spectrum, pero esa opción nos podría resultar realmente incómoda por usabilidad y gestión de los datos (se tendría que trabajar en un emulador o la máquina real y los datos sólo se podrían exportar a cinta o a TAP/TZX).

Lo ideal es utilizar un Editor de Sprites nativo de nuestra plataforma cruzada de desarrollo que permita el dibujado en un entorno cómodo y la exportación de los datos a código “.asm” (ristras de DBs) que incluir directamente en nuestro ensamblador.

Nuestra elección principal para esta tarea es SevenuP, de metalbrain. Nos decantamos por SevenuP por su clara orientación al dibujo “al pixel” y sus opciones para el programador, especialmente el sistema de exportación de datos a C y ASM y la gestión de máscaras y frames de animación. Además, SevenuP funciona bajo múltiples Sistemas Operativos, siendo la versión para Microsoft Windows emulable también en implementaciones como WINE de GNU/Linux.

Para el propósito de este capítulo (y, en general durante el proceso de creación de un juego), dibujaremos en SevenuP nuestro spriteset con los sprites distribuídos verticalmente (cada sprite debajo del anterior). Crearemos un nuevo “sprite” con File → New e indicaremos el ancho de nuestro sprite en pixels y un valor para la altura que nos permita alojar suficientes sprites en nuestro tileset. 



.. figure:: gfx3_sevenup_vertical.png
   :scale: 50%
   :align: center
   :alt: Gráficos en vertical

   Gráficos en vertical


Por ejemplo, para guardar la información de 10 sprites de 16×16 crearíamos un nuevo sprite de 16×160 píxeles. Si nos vemos en la necesidad de ampliar el sprite para alojar más sprites podremos “cortar” los datos gráficos, crear una imagen nueva con un tamaño superior y posteriormente pegar los datos gráficos cortados. La documentación de SevenUp explica cómo copiar y pegar::

    Modo de Selección 1:
    ====================

    Set Pixel/Reset Pixel
    El botón izquierdo pone los pixels a 1.
    El botón derecho pone los pixels a 0.
    Atajo de teclado: 1


    Modo de Selección 2:
    ====================

    Toggle Pixel/Select Zone
    El botón izquierdo cambia el valor de los pixels entre 0 y 1.
    El botón derecho controla la selección. Para seleccionar una zona,
    se hace click-derecho en una esquina, click-derecho en la opuesta y ya
    tenemos una porción seleccionada. La zona seleccionada será algo mas
    brillante que la no seleccionada y las rejillas (si están presentes)
    se verán azules. Ahora los efectos solo afectarán a la zona seleccionada,
    y se puede copiar esta zona para pegarla donde sea o para usarla como
    patrón en el relleno con textura. Un tercer click-derecho quita la
    selección:

    Atajo de teclado: 2

    Copy
    Copia la zona seleccionada (o el gráfico completo si no hay zona seleccionada)
    a la memoria intermedia para ser pegada (en el mismo gráfico o en otro) o para
    ser usada como textura de relleno. Atajo de teclado: CTRL+C.

    Paste
    Activa/desactiva el modo de pegado, que pega el gráico de la memoria intermedia
    a la posición actual del ratón al pulsar el botón izquierdo. Los atributos solo
    se pegan si el pixel de destino tiene la misma posición dentro del carácter que
    la fuente de la copia. Con el botón derecho se cancela el modo de pegado. Atajo
    de teclado: CTRL+V.

Otra opción es trabajar con un fichero .sev por cada sprite del juego, aprovechando así el soporte para “fotogramas” de SevenuP. No obstante, suele resultar más cómodo mantener todos los sprites en un único fichero con el que trabajar ya que podemos exportar todo con una única operación y nos evita tener que “mezclar” las múltiples exportaciones de cada fichero individual.

Mediante el ratón (estando en modo 1) podemos activar y desactivar píxeles y cambiar el valor de tinta y papel de cada recuadro del Sprite. El menú de máscara nos permite definir la máscara de nuestros sprites, alternando entre la visualización del sprite y la de la máscara.

El menú de efectos nos permite ciertas operaciones básicas con el sprite como la inversión, rotación, efecto espejo horizontal o vertical, rellenado, etc.

Es importante que guardemos el fichero en formato .SEV pues es el que nos permitirá realizar modificaciones en los gráficos del programa y una re-exportación a ASM si fuera necesario.

Antes de exportar los datos a ASM, debemos definir las opciones de exportación en File → Output Options:



.. figure:: gfx3_opciones_export_su.png
   :scale: 50%
   :align: center
   :alt: Opciones de exportación.

   Opciones de exportación.


