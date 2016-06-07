# Guisse: Gnuplot User Interpreter Suggested for Student's Experimentation

Guisse is just a small editor that helps to work with GNUplot. It does not provides GNUplot, it does not plot by itself, but it communicates with GNUplot in a very simple way. Therefore, it does require GNUplot in order to work.

## Considerations?

* It still is in development phase, so there is not guaranty that it will work

* If you work with Windows, there is warranty that it will not work. It is in development phase, remember?.

## How does it work?

* After you click the plot/export button and before the plot gets completed, the system will create a template and include it before your script, then that final bigger-script is send to GNUplot in order to plot it.

## Features

* Templateing: it has the option to select within some templates in order to have consistent plots from one project to another or within big projects. 

* Pre-seted commands: it has a very small library with some often used commands in a template fashion, select and insert in your project.

* Xfig output : if you use Linux, you can export to Xfile format directly. It does not use the normal GNUplot terminal, but a different process: it exports the image to EPS (which is nicer than the Xfig terminal) and invites the OS to a dinner and and ask for a Xfig conversion using “pstoedit”. So you need “pstoedit” in order to use this feature. 

* LaTeX friendly: it can replace strings inside the xfig file for LaTeX labels, that ensures the same font within the document. l/um:$\lambda/si\{\nano\meter}$ will change the string "l/um" to "$\lambda/si\{\nano\meter}$" which is latex compatible.

### Missing features?

* A proper setup option: it requires several packages that are not standard in python systems, so they must be installed manually... sorry about that 

* Better architecture: the main windows has the methods used for plotting, those must be moved to somewhere else. It is horrible programmed... It is in development phase, remember?.

* Some menus need actions... sorry about that too... development phase...

### planned features?

* PDF export: it will export the Xfig files to PFD since some latex users do not use xfig because “it is ugly and old”.

## Requirements

* Linux Based System

* PyQt

* Gnuplot

* pstoedit



## Installation

Basically run the run.sh file and let the system complain and tell you what you need to install. Since it still is a quick an dirty solution it has not an installer
