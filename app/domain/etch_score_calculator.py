from __future__ import annotations

import math


class EtchScoreCalculator:
    # Calibration percentiles
    P5: float = 0.000000e+00
    P95: float = 7.867448e+17

    def calculate(self, ion_flux: float, ion_energy: float) -> float:
        """
        Args:
            ion_flux: ion flux [cm^-2 s^-1]
            ion_energy: ion energy [eV]
        Returns:
            etch_score [0–100 point]
        """
        raw = ion_flux * math.sqrt(max(ion_energy - 20.0, 0.0))

        if self.P95 == self.P5:
            return 0.0

        normalized = (raw - self.P5) / (self.P95 - self.P5) * 100.0
        return max(0.0, min(100.0, normalized))
