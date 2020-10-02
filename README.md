# gnuplot-in-the-browser

[Gnuplot](http://www.gnuplot.info/) is a powerful command line plotting program that can be used for quick data analysis or publication quality figures. This project provides some scripts for downloading and compiling
Gnuplot to WebAssembly so that it can run in the browser. The source for an [example website](http://hostcat.fhsu.edu/cdclark/static/apps/gnuplot/) is included.

The motivation for this project was the [Gnuplotter](http://gnuplot.respawned.com/) website. It does the same thing, but hasn't been updated is several years and uses Gnuplot version 4. I wanted to be able to give
students access to Gnuplot 5 (which has some improved features when it comes to function fitting) without requiring them to install anything, so I learned how to build WebAssembly apps from command line applications.

## Quickstart

To build the application, you need to have install the [Emscripten SDK](https://emscripten.org/docs/getting_started/downloads.html). Then run the build script

```bash
$ bash ./build.sh
```

This will download Gnuplot, configure it for an emscripten build, build the WebAssymbly module, and copy all the files needed to run the website into a "deploy" directory. The contents of the deploy directory can be copied
directly to a web server.

Two apps are build, one that provides a
simple interface to the [Gnuplot command line](http://hostcat.fhsu.edu/cdclark/static/apps/gnuplot/), and another that is designed to let students to simple [linear regression](http://hostcat.fhsu.edu/cdclark/static/apps/linear-regression/) without any Gnuplot knowledge.
