#! /bin/bash


set -e

ROOT=$PWD
BUILD=$ROOT/build


mkdir -p $BUILD

cd $BUILD

GNUPLOT_VERSION="5.4.0"
if [[ ! -e gnuplot-${GNUPLOT_VERSION}.tar.gz ]]
then
  wget https://sourceforge.net/projects/gnuplot/files/gnuplot/${GNUPLOT_VERSION}/gnuplot-${GNUPLOT_VERSION}.tar.gz/download
  mv download gnuplot-${GNUPLOT_VERSION}.tar.gz
fi

if [[ ! -d gnuplot-${GNUPLOT_VERSION} ]]
then
  tar xzf gnuplot-${GNUPLOT_VERSION}.tar.gz
fi

cd gnuplot-${GNUPLOT_VERSION}

if [[ ! -e src/gnuplot ]]
then
emconfigure ./configure \
  --disable-largefile \
  --disable-plugins \
  --disable-history-file \
  --disable-x11-mbfonts \
  --disable-x11-external \
  --disable-raise-console \
  --disable-wxwidgets \
  --disable-stats \
  --without-libcerf \
  --without-latex \
  --without-kpsexpand \
  --without-x \
  --without-x-dcop \
  --without-aquaterm \
  --without-readline \
  --without-lua \
  --with-cwdrc \
  --without-row-help \
  --without-wx-multithreaded \
  --without-bitmap-terminals \
  --without-tektronix \
  --without-gpic \
  --without-tgif \
  --without-mif \
  --without-regis \
  --without-cairo \
  --without-qt

emmake make gnuplot
fi

cd ${ROOT}

if [[ ! -d gnuplot-deploy ]]
then
  mkdir gnuplot-deploy
fi

if [[ ! -d linear-regression-deploy ]]
then
  mkdir linear-regression-deploy
fi

cp ${BUILD}/gnuplot-${GNUPLOT_VERSION}/src/gnuplot gnuplot-deploy/gnuplot.js
cp ${BUILD}/gnuplot-${GNUPLOT_VERSION}/src/gnuplot.wasm gnuplot-deploy/
cp -r ${BUILD}/gnuplot-${GNUPLOT_VERSION}/term/js/ gnuplot-deploy/files
cp www/gnuplot/index.html gnuplot-deploy/
cp www/fhsu-logo.png gnuplot-deploy/

cp ${BUILD}/gnuplot-${GNUPLOT_VERSION}/src/gnuplot linear-regression-deploy/gnuplot.js
cp ${BUILD}/gnuplot-${GNUPLOT_VERSION}/src/gnuplot.wasm linear-regression-deploy/
cp www/linear-regression/index.html linear-regression-deploy/
cp www/fhsu-logo.png linear-regression-deploy/

