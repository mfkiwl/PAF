# SPDX-FileCopyrightText: <text>Copyright 2021,2022 Arm Limited and/or its
# affiliates <open-source-office@arm.com></text>
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This file is part of PAF, the Physical Attack Framework.

from setuptools import setup, find_packages

setup(
        name="run-model",
        version="0.1",
        packages=['FI', 'PAF'],
        install_requires=[
          'pyyaml==5.4.1',
          'pyelftools==0.26',
          'tqdm==4.50.0'
        ],
        scripts=['run-model.py', 'campaign.py', 'generate-xref.py'],
)
