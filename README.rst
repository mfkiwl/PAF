..
  SPDX-FileCopyrightText: <text>Copyright 2021,2022 Arm Limited and/or its
  affiliates <open-source-office@arm.com></text>
  SPDX-License-Identifier: Apache-2.0

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  This file is part of PAF, the Physical Attack Framework.

|BadgeLicence| |CIUbuntu2004gcc| |CIUbuntu2004clang|

.. |BadgeLicence| image:: https://img.shields.io/github/license/ARM-software/PAF
   :alt: PAF licence
   :target: https://github.com/ARM-software/PAF/blob/main/LICENSE.txt

.. |CIUbuntu2004gcc| image:: https://github.com/ARM-software/PAF/actions/workflows/ubuntu-2004-gcc.yml/badge.svg
   :alt: Last build status on Ubuntu 20.04 with gcc
   :target: https://github.com/ARM-software/PAF/actions/workflows/ubuntu-2004-gcc.yml

.. |CIUbuntu2004clang| image:: https://github.com/ARM-software/PAF/actions/workflows/ubuntu-2004-clang.yml/badge.svg
   :alt: Last build status on Ubuntu 20.04 with clang
   :target: https://github.com/ARM-software/PAF/actions/workflows/ubuntu-2004-clang.yml

===============================================================================
PAF, the Physical Attack Framework
===============================================================================

Welcome to PAF ! PAF is a suite of tools and libraries to learn about physical
attacks, such as fault injection and side channels, and hopefully help harden
code bases against those threats.

Requirements
============

To build PAF from source, you will need a C++ compiler compatible with C++14,
and `CMake <https://cmake.org/>`_.

A significant number of the PAF tools assumes that you at least have access to
Tarmac traces. These are detailed traces of a program's execution, and they
are generated by a number of Arm products, like software models of CPUs (e.g.
FastModel).

PAF has the capability to directly drive a FastModel and perform a number of
analysis. In order to use this capability, you will need to have access to a
`FastModel
<https://developer.arm.com/tools-and-software/simulation-models/fast-models>`_


Building
========

The simplest way to build PAF is:

.. code-block:: bash

  $ cmake .
  $ cmake --build .

A slightly more evolved way of building and testing PAF, in release mode with
debug info, using the ``clang`` compiler, ``Ninja`` build system and producing
a ``compile_commands.json`` file looks like:

.. code-block:: bash

  $ CC=clang CXX=clang++ cmake -S . -B build -G Ninja \
         -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo \
         -DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=ON
  $ ln -s build/compile_commands.json .
  $ ninja -C build/
  $ ninja -C build/ test

Testing
=======

PAF contains both unit testing and application level testing. Unit testing can
be performed using the ``test`` target, with no external dependencies.
Application level testing is a different story as it requires access to a
cross-compiler and a FastModel. If you have access to those, ``CMake`` can
setup a test environment for you with:

.. code-block:: bash

  $ CC=clang CXX=clang++ cmake -S . -B build -G Ninja \
         -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo \
         -DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=ON \
         -DFVP_MODEL_DIR:PATH=/opt/FastModels/11.12/FVP_MPS2_Cortex-M3_CC312/models/Linux64_GCC-6.4/FVP_MPS2_Cortex-M3_CC312 \
         -DFVP_PLUGINS_DIR:PATH=/opt/FastModels/11.12/FastModelsPortfolio_11.12/plugins/Linux64_GCC-6.4 \
         -DARM_GCC_INSTALL_DIR:PATH=/opt/gcc-arm-none-eabi-10-2020-q4-major

Usage and documentation
=======================

For more information on PAF, the tools it provides and how to use them, see the
`main documentation <doc/index.rst>`_.

License
=======

PAF is distributed under the `Apache v2.0 License
<http://www.apache.org/licenses/LICENSE-2.0>`_.

Third party software
====================

PAF requires third party software that is not included in PAF's source code
repository. PAF's configure and build system, `CMake`, will automatically
download, configure and build this third party software. As each of those
third party software comes with its own specific license, you have to check
their licenses comply with your own specific requirements.

The third party software used by PAF is:

- `tarmac-trace-utilities <https://github.com/ARM-software/tarmac-trace-utilities>`_,
  licensed under https://github.com/ARM-software/tarmac-trace-utilities/blob/main/LICENSE.txt,
  is the library that provides PAF with the fondations for efficiently manipulating tarmac traces.

- `pyyaml <https://pypi.org/project/PyYAML/>`_,
  and `pyelftools <https://pypi.org/project/pyelftools/>`_,
  and `tqdm <https://pypi.org/project/tqdm/>`_ are used by ``run-model.py`` and ancillary tools.
  
- `GoogleTest <https://github.com/google/googletest>`_,
  licensed under https://github.com/google/googletest/blob/main/LICENSE,
  is the unit testing framework used by PAF.

- `numpy <https://numpy.org/>`_, licensed under https://github.com/numpy/numpy/blob/main/LICENSE.txt,
  is used by some unit tests.

Feedback, contributions and support
===================================

Please use the GitHub issue tracker associated with this repository for feedback.

Code contributions are most welcomed. Please make sure they stick to the style
used in the rest of the PAF code and submit them via GitHub pull requests. 
