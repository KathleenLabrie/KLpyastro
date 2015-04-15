Install module
==============
Make sure that your installation location is in the PYTHONPATH before you 
install.  It is a setuptools requirement. ::

	python setup.py install --prefix=<somewhere>

with <somewhere>/lib/python2.7/site-packages in the PYTHONPATH.  (Of course,
change the 'python2.7' to match your Python version.)


Build documentation
===================
The latest documentation is available at ::
 
	http://KLpyastro.readthedocs.org/en/latest/

If you need to build documentation, eg. need a local copy, ::

	python setup.py build_sphinx

will build the html documentation in ::

	docs/KLpyastro_Manual/_build/html

Point your browser to ::

	docs/KLpyastro_Manual/_build/html/index.html

If you are interested in a PDF version: ::

	cd docs/KLpyastro_Manual
	make latexpdf

The PDF is ::

	docs/KLpyastro_Manual/_build/latexpdf/KLpyastro_Manual.pdf


Installing the documentation somewhere convenient
=================================================

The documentation is included in the egg, but it is not
really accessible.  The documentation is also in the source code
but you will probably want to delete that once you've installed
the module.

To extract the documentation and copy it somewhere useful, ::

   (from source code):
      klpyastro/getdocs.py /your/preferred/path
   (from installed egg):
      <where_egg_is_located>/klpyastro-0.1.0dev1-py2.7.egg/klpyastro/getdocs.py

will copy the documentation to /your/preferred/path/klpyastro.




