# TaTeTi
Juego de TaTeTi en RED

Descripción: tateti con interfaz gráfica y menu de selección para jugar contra una computadora, dos jugadores en la misma pc, o dos jugadores a travez de una comunicación de tipo cliente/servidor-servent. Si se conoce la ip pública del servidor y éste abre el puerto que va a usar desde el modem(tcp) también se puede jugar a travez de internet. Se puede jugar en windows y linux, pero por ahora la parte de red solo para linux. 

Es necesario tener instalado los siguientes paquetes de python:
pygame : para la interfaz gráfica
twisted : framework de red 

Posibles mejoras: 
        -refactorización del código
        -cambiar los threads por clases y bombear el reactor de twisted
        
        
Si se tiene problemas para instalar twisted descargarlo aquí https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted e instalar con pip, 'pip install *.whl'
