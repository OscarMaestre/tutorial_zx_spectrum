Prologo
==================

Mucha gente se preguntará cómo es posible que, en pleno 2011, exista alguien con interés en escribir y publicar un curso sobre esta temática. Apenas un par de centenares o miles de personas en todo el mundo pueden estar realmente interesadas en la lectura de un curso como este.

Sin embargo, he dedicado gran cantidad de horas a escribir y depurar este texto y sus ejemplos. ¿El motivo? Simplemente, no se me ocurre una mejor forma de concentrar en un único elemento mi pasión por el ZX Spectrum, la programación en ensamblador, el desarrollo de programas y los videojuegos.

Puedo y debo decir que el ZX Spectrum cambió mi vida. Aquella tarde de viernes de 1989 en la que mis padres aparecieron por la puerta con un Spectrum +2A de segunda mano, junto a una caja llena de revistas Microhobby y cintas de juegos y programas, cambió el que hubiera sido mi futuro profesional, orientándolo hacia el mundo de la Ingeniería, la Electrónica y las Telecomunicaciones.

Como todos, empecé exprimiendo el Spectrum a través de los juegos profesionales que se vendían para la popular máquina de Sinclair. En paralelo a los juegos, comencé a leer los ejemplares de las revistas Microhobby que habíamos adquirido junto al ordenador.

Mi relación inicial con Microhobby fue las que supongo que tendrían muchos usuarios sin interés por la programación: directo a las páginas con análisis, fotos y notas de juegos. Como mucho, como curiosidad tecleaba alguno de los listados en BASIC de la sección de trucos, maravillándome con sencillas melodías, o psicodélicos efectos de colores con el borde.

Esos listados en BASIC, tan sencillos, despertaron mi curiosidad por “cómo se hacen estos juegos”. Poco a poco se produjo el cambio: mi interés por jugar pasó a ser interés, mucho interés, por desarrollar.

Microhobby fue la herramienta mediante la cual aprendí BASIC y ensamblador de Z80. Como la completa revista que era, entre sus páginas de análisis de juegos podías encontrar fantásticos artículos y listados animándote a programar pequeñas rutinas y juegos.

Casi sin darme tiempo para disfrutar de lo que estaba aprendiendo, llegó el fin de la revista Microhobby y el ocaso comercial del Spectrum en España. Las consolas ocuparon el espacio lúdico del Spectrum y el PC se convirtió en la herramienta de programación estándar. El Spectrum pasó para mí al olvido hasta que la revista Micromanía publicó el emulador “SPECTRUM” de Pedro Gimeno.

Este emulador, y todos los que aparecieron en la década de los 90, sirvió para que la gente no olvidara el Spectrum y todo el legado que nos había dejado.

Ya a principios del siglo XXI, el Spectrum volvió a ser mi centro de atención: inicialmente, desarrollé el emulador ASpectrum con el que mejoré en gran parte mis conocimientos sobre la arquitectura del Spectrum y la programación en lenguaje ensamblador de Z80.

Una vez ASpectrum fue una realidad, comencé a realizar sencillos juegos con Z88DK en C con pequeñas rutinas en ensamblador integradas en el código. Se despertó de nuevo en mí el interés por desarrollar juegos de Spectrum y de escribir tutoriales y cursos con todo lo que iba rememorando o aprendiendo.

En esa época (años 2002 - 2003) se fundó Compiler Software y se editó la revista MagazineZX en el portal Speccy.org, incluyendo diversos cursos de programación en C con Z88DK y en ensamblador de Z80 con pasmo. Estos cursos, finalmente, se han ampliado y materializado en el texto que estáis leyendo. 


Objetivos y desarrollo del curso

El objetivo principal de este curso, libro, o gran tutorial es que un lector con conocimientos básicos de programación pueda aprender fácilmente ensamblador de Z80 aplicado al desarrollo de juegos y utilidades de Spectrum.

Con este curso pretendemos enseñar al lector:


* La arquitectura del Sinclair ZX Spectrum: se describen sus componentes internos y cómo se interrelacionan.
* La arquitectura del microprocesador Z80: sus registros y su juego de instrucciones.
* La sintaxis del lenguaje ensamblador de Z80: nmemónicos del lenguaje.
* Cómo utilizar el ensamblador PASMO para ensamblar nuestros programas en ASM de Z80.
* Acceso a los periféricos del Spectrum: Teclado, Joystick, etc.
* Gráficos en el Spectrum: Sprites, Fuentes de texto, Impresión de mapeados, etc.
* Funciones avanzadas de los modelos 128K: paginación de memoria.
* Rutinas auxiliares: subrutinas de carga, compresión RLE, interrupciones del procesador.
* Subrutinas útiles para el desarrollo de programas.


Al escribirlo he intentado ponerme en la piel del programador que desea empezar con el lenguaje ensamblador, por lo que los dos primeros capítulos describen la arquitectura del Spectrum y del Z80. Los siguientes cinco capítulos tratan sobre la sintaxis del lenguaje ensamblador, donde el lector aprenderá las “piezas básicas” con las que construir programas en ensamblador para cualquier microordenador basado en el procesador Z80 de Zilog.

A partir del octavo capítulo nos centramos única y exclusivamente en el Spectrum, profundizando en todas las diferentes áreas que puedan sernos de utilidad para el desarrollo de juegos o programas: lectura del teclado, temporización, impresión de gráficos, técnicas de mapeado, carga desde cinta, etc.

A lo largo del texto se presentan múltiples ejemplos y rutinas para que el lector pueda verificar la teoría descrita así como utilizarlas directamente en sus propios programas.

Cuando se escribe una rutina para un procesador tan “limitado” como el Z80 suelen presentarse 2 opciones: escribir una rutina comprensible, o escribir una rutina optimizada. El objetivo del curso es que el lector aprenda programación en ensamblador y por lo tanto debe de poder comprender las rutinas que se presentan, por lo que en el desarrollo de los ejemplos y las rutinas ha primado la comprensión frente a la optimización en aquellos casos en que ambas opciones chocaban.

Esto no quiere decir que las rutinas no sean óptimas: al contrario, se han diseñado para que sean siempre lo más óptimas posible siempre y cuando eso no implique hacerlas incomprensibles para el lector. Aún así, un programador avanzado podrá (y deberá) darles una pequeña vuelta de tuerca adicional para exprimir ciclos de reloj a la rutina y hacerla aún un poco más rápida. Ese podría ser el objetivo del lector una vez acabado el curso y de cara al diseño de un programa.

Si un lector sin conocimientos de ensamblador, tras leer el curso, acaba decidiendo programar un juego y utiliza o mejora las rutinas que se presentan en este texto, podremos decir que el curso ha conseguido su objetivo.

Espero que disfrutéis tanto leyéndolo como yo escribiéndolo.
