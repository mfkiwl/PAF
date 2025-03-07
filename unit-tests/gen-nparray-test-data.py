#!/usr/bin/env python3
# SPDX-FileCopyrightText: <text>Copyright 2022 Arm Limited and/or its
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

import argparse
import numpy as np
import os
import sys


class Matrix:

    def __init__(self, name, ty, rows, cols, cmd_line):
        self.M = np.random.rand(rows, cols)
        self.rows = rows
        self.cols = cols
        self.name = name
        self.ty = ty
        self.checker = "C_{}".format(name)
        self.cmd_line = cmd_line

    def matrix(self, indent):
        t = indent * ' '
        lines = list()
        lines.append(t + "const NPArray<{}> {}(".format(self.ty, self.name))
        lines.append(t+t + "{")
        for row in self.M:
            lines.append(t+t+t + ", ".join("{:1.8f}".format(e) for e in row)+',')
        lines.append(t+t + "},");
        lines.append(t+t + "{}, {});".format(self.rows, self.cols))
        return lines

    def expected(self, t, comment, s, last=False):
        lines = list()
        lines.append(t + "/* {}: */".format(comment))
        l = "{{{}}}".format(", ".join("{:1.8f}".format(e) for e in s))
        if not last:
            l += ','
        lines.append(t + l)
        return lines
        
    def sum(self, indent):
        t = indent * ' '
        lines = list()
        lines.append(t + "const SumChecker<{}, {}, {}> {}(".format(self.ty,
                     self.rows, self.cols, self.checker))
        lines.append(
            t+t + "{},".format(self.name))
        lines.extend(self.expected(t+t, "sums, by row",
                     np.sum(self.M, axis=1)))
        lines.extend(self.expected(t+t, "sums, by col",
                     np.sum(self.M, axis=0), True))
        lines.append(t + ");")
        return lines

    def mean(self, indent):
        t = indent * ' '
        lines = list()
        lines.append(t + "const MeanChecker<{}, {}, {}> {}(".format(self.ty,
                     self.rows, self.cols, self.checker))
        lines.append(
            t+t + "{},".format(self.name))
        lines.extend(self.expected(t+t, "means, by row",
                     np.mean(self.M, axis=1)))
        lines.extend(self.expected(t+t, "means, by col",
                     np.mean(self.M, axis=0)))
        lines.extend(self.expected(t+t, "var0, by row",
                     np.var(self.M, axis=1, ddof=0)))
        lines.extend(self.expected(t+t, "var1, by row",
                     np.var(self.M, axis=1, ddof=1)))
        lines.extend(self.expected(t+t, "var0, by col",
                     np.var(self.M, axis=0, ddof=0)))
        lines.extend(self.expected(t+t, "var1, by col",
                     np.var(self.M, axis=0, ddof=1)))
        lines.extend(self.expected(t+t, "stddev, by row",
                     np.std(self.M, axis=1)))
        lines.extend(self.expected(t+t, "stddev, by col",
                     np.std(self.M, axis=0), True))
        lines.append(t + ");")
        return lines

    def student(self, indent):
        t = indent * ' '
        lines = list()
        lines.append(t + "const StudentChecker<{}, {}, {}> {}(".format(self.ty,
                     self.rows, self.cols, self.checker))
        lines.append(
            t+t + "{},".format(self.name))
        m0 = np.random.rand(1, self.cols)
        lines.extend(self.expected(t+t, "m0", m0[0]))
        m = np.mean(self.M, axis=0)
        v = np.var(self.M, axis=0, ddof=1)
        tvalues = np.sqrt(self.rows) * (m - m0) / np.sqrt(v)
        lines.extend(self.expected(t+t, "tvalues", tvalues[0], True))
        lines.append(t + ");")
        return lines

    def test_header(self, t):
        lines = list()
        lines.append(t + "// clang-format off")
        lines.append(
            t + "// === Generated automatically with '{}'".format(self.cmd_line))
        return lines

    def test_tail(self, t):
        lines = list()
        lines.append(
            t + "// === End of automatically generated portion")
        lines.append(t + "// clang-format on")
        return lines

    def emit(self, test):
        indent = 4
        t = indent * ' '
        lines = list()
        lines.extend(self.test_header(t))
        lines.extend(self.matrix(indent))
        test = getattr(self, test)
        lines.extend(test(indent))
        lines.extend(self.test_tail(t))
        return "\n".join(lines)

def main():
    usage = """Usage: %(prog)s [options] TEST

%(prog)s generates matrices for testing the NPArray / SCA functionality,
like mean, variance, standard deviation, ...

"""
    _version = "0.0.0"
    _copyright = "Copyright 2022 Arm Limited. All Rights Reserved."
    _prog = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("-v", "--verbose",
                        help="Be more verbose, may be specified multiple times.",
                        action='count',
                        default=0)
    parser.add_argument("-V", "--version",
                        help="Print the version number of this tool.",
                        action='version',
                        version='%(prog)s ({version}) {copyright}'.format(version=_version, copyright=_copyright))
    parser.add_argument("-r", "--rows",
                        metavar='NUM_ROWS',
                        type=int,
                        help="Set the matrix number of rows to NUM_ROWS (default: %(default)s)",
                        default=4)
    parser.add_argument("-c", "--columns",
                        metavar='NUM_COLUMNS',
                        type=int,
                        help="Set the matrix number of columns to NUM_COLUMNS (default: %(default)s)",
                        default=4)
    parser.add_argument("-n", "--name",
                        metavar='NAME',
                        help="Set the matrix name to NAME (default: %(default)s)",
                        default="a")
    parser.add_argument("-t", "--type",
                        metavar='TYPE',
                        help="Set the matrix element type to TYPE (default: %(default)s)",
                        default="double")
    parser.add_argument("TEST",
                        choices=['mean', 'sum', 'student'],
                        help="Generate expected values for TEST")
    options = parser.parse_args()

    M = Matrix(options.name, options.type, options.rows, options.columns,
               "{} --rows {} --columns {} {}".format(_prog, options.rows, options.columns, options.TEST))
    print(M.emit(options.TEST))

    return 0

if __name__ == '__main__':
    sys.exit(main())