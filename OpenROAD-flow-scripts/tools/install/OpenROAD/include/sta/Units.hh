// OpenSTA, Static Timing Analyzer
// Copyright (c) 2025, Parallax Software, Inc.
// 
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.
// 
// The origin of this software must not be misrepresented; you must not
// claim that you wrote the original software.
// 
// Altered source versions must be plainly marked as such, and must not be
// misrepresented as being the original software.
// 
// This notice may not be removed or altered from any source distribution.

#pragma once

#include <string>

namespace sta {

class Unit
{
public:
  Unit(const char *suffix);
  Unit(float scale,
       const char *suffix,
       int digits);
  // Convert from sta units to user interface units.
  double staToUser(double value);
  // Convert from user interface units to sta units.
  double userToSta(double value);
  void operator=(const Unit &unit);
  float scale() const { return scale_; }
  void setScale(float scale);
  const char *scaleAbbreviation() const;
  const char *suffix() const { return suffix_.c_str(); }
  // scale abbreviation + suffix
  const char *scaledSuffix() const { return scaled_suffix_.c_str(); }
  void setSuffix(const char *suffix);
  int digits() const { return digits_; }
  void setDigits(int digits);
  // Does not include suffix.
  int width() const;
  const char *asString(float value) const;
  const char *asString(double value) const;
  const char *asString(float value,
		       int digits) const;

private:
  void setScaledSuffix();

  float scale_;			// multiplier from user units to internal units
  std::string suffix_;		// print suffix
  std::string scaled_suffix_;
  int digits_;			// print digits (after decimal pt)
};

// User interface units.
// Sta internal units are always seconds, farads, volts, amps.
class Units
{
public:
  Units();
  Unit *find(const char *unit_name);
  void operator=(const Units &units);
  Unit *timeUnit() { return &time_unit_; }
  const Unit *timeUnit() const { return &time_unit_; }
  Unit *capacitanceUnit() { return &capacitance_unit_; }
  const Unit *capacitanceUnit() const { return &capacitance_unit_; }
  Unit *voltageUnit() { return &voltage_unit_; }
  const Unit *voltageUnit() const { return &voltage_unit_; }
  Unit *resistanceUnit() { return &resistance_unit_; }
  const Unit *resistanceUnit() const { return &resistance_unit_; }
  Unit *currentUnit() { return &current_unit_; }
  const Unit *currentUnit() const { return &current_unit_; }
  Unit *powerUnit() { return &power_unit_; }
  const Unit *powerUnit() const { return &power_unit_; }
  Unit *distanceUnit() { return &distance_unit_; }
  const Unit *distanceUnit() const { return &distance_unit_; }
  Unit *scalarUnit() { return &scalar_unit_; }
  const Unit *scalarUnit() const { return &scalar_unit_; }

private:
  Unit time_unit_;
  Unit resistance_unit_;
  Unit capacitance_unit_;
  Unit voltage_unit_;
  Unit current_unit_;
  Unit power_unit_;
  Unit distance_unit_;
  Unit scalar_unit_;
};

} // namespace
