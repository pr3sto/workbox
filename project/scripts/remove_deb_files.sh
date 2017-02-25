#!/bin/bash

/bin/rm -f preinst
/bin/rm -f postinst
/bin/rm -f prerm
/bin/rm -f postrm
/bin/rm -f make_deb_package.sh
/bin/rm -rf debian/
/bin/rm -f ../${PWD##*/}_*
/bin/rm -f ../${PWD##*/}-*
/bin/rm -f -- "$0"
