Nominal Unification
===========

|Build Status|

A python library implementing nominal unification.

Examples
--------

nominal_unification, in many ways, acts like the unification library.

.. code-block:: python

   >>> from nominal_unification import *
   >>> unify(1, 1)
   {}
   >>> unify(1, 2)
   False
   >>> unify((1, Var('x')), (1, 2))
   {'x': 2}
   >>> unify((Var('x'), Var('x')), (1, 2))
   False

It also has the ability to perform unification modulo variable bindings.

.. code-block:: python

   >>> unify(Abs('x', 'x'), Abs('z', Var('Z')))
   {'Z', 'z'}
   >>> unify(("x", Abs("x", "x")), (Var("Y"), Abs("z", Var("Y"))))
   False

Author
------

`Anthony Hart`_


Citations
--------

The theory underlying this implementation comes from the paper "Efficiency of a good but not linear nominal unification algorithm": https://easychair.org/publications/preprint/DLVk

This implementation was frequently used as a reference early on, though the current version has diverged significantly: https://github.com/sgraf812/nominal-unification

.. |Build Status| image:: https://travis-ci.org/mrocklin/unification.png
   :target: https://travis-ci.org/mrocklin/unification
