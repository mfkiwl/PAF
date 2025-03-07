/*
 * SPDX-FileCopyrightText: <text>Copyright 2021,2022 Arm Limited and/or its
 * affiliates <open-source-office@arm.com></text>
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * This file is part of PAF, the Physical Attack Framework.
 */

#include "PAF/SCA/Noise.h"

namespace PAF {
namespace SCA {

std::unique_ptr<NoiseSource> NoiseSource::getSource(Type noiseTy,
                                                    double noiseLevel) {
    switch (noiseTy) {
    case NoiseSource::Type::ZERO:
        return std::unique_ptr<PAF::SCA::NoiseSource>(
            new PAF::SCA::NullNoise());
    case NoiseSource::Type::UNIFORM:
        return std::unique_ptr<PAF::SCA::NoiseSource>(
            new PAF::SCA::UniformNoise(noiseLevel));
    case NoiseSource::Type::NORMAL:
        return std::unique_ptr<PAF::SCA::NoiseSource>(
            new PAF::SCA::NormalNoise(noiseLevel));
    }
}

} // namespace SCA
} // namespace PAF
