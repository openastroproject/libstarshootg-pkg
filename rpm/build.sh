#!/bin/bash

cp ../patches/*.patch .
rm -f makefile.patch

rm -f libstarshootg-*.tar.gz
ln ../libstarshootg-*.tar.gz .
rel=`cut -d' ' -f3 < /etc/redhat-release`
fedpkg --release f$rel local
