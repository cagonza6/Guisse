set angles degrees
set border 0 ls 1 # no figure borders

# dibuja los ejes como flechas

set arrow 1 from   0,-0.5 to  0,40 arrowstyle 1# X-axis
set arrow 2 from  -0.5,0   to 85,0 arrowstyle 1# Y-axis

# Label Origin
set label at -0.25,-0.25 '0'

#Elimina los label de los ejes y coloca etiquetas definidas por el user, mas facil que moverlos
set ylabel 'y(x)'
set xlabel 'X'

### Tics
set xtics axis in scale 0.5,0.25 mirror norotate  offset character 0, 0, 0 autojustify
set ytics axis in scale 0.5,0.25 mirror norotate  offset character 0, 0, 0 autojustify

#rango en el que se plot range
set xrange [0:85]
set yrange [0:40]

### Herramientas
##defino la funcion a usar
g=9.8
v0=30
alpha=60
h0=0
t(x)=x/(v0*cos(alpha))
y(x)=-g/2*(t(x))**2+v0*sin(alpha)*t(x)+h0
h(x)=-g/2*((x))**2+v0*sin(alpha)*(x)+h0

#puntos importantes, los usare despues para definir cosas
x1=v0*v0*sin(2*alpha)/2/g
y1=y(x1)

g(x) = (x >= 0 && x <= 2*x1) ? y(x) : 1/0

# defino dos rectas para cada punto importante, defino sus coordenadas en base a los puntos anteriores
#lineas verticales
set arrow 3 from x1,0       to x1, g(x1)  arrowstyle 13 dt 2# line
set arrow 4 from  0 ,g(x1) to x1, g(x1)  arrowstyle 13 dt 2# line

#Etiquetas varias
set label at x1+1,2 'xm2'
set label at x1*2+1,2 'xm'
set label at x1,y(x1)+2  'ym'

### Plot ################################
# aqui viene lo importante, defino el plot de la figura y agrego los puntos importantes.
plot y(x) title '$y(x)$' w lines ls 6,'-' title '' with points pt 7 lc 6,'-' title '' with points pt 7 lc 6,'-' title '' with points pt 7 lc 6
39.76 0
e
79.53 0
e
39.76 34.43
e