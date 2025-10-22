"""Time signature support for polyrhythmic patterns."""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class TimeSignature:
    """Represents a musical time signature.

    Attributes:
        numerator: Number of beats per measure (top number)
        denominator: Note value that gets one beat (bottom number)
        name: Human-readable name
    """
    numerator: int
    denominator: int
    name: str = ""

    def __post_init__(self):
        """Generate name if not provided."""
        if not self.name:
            self.name = f"{self.numerator}/{self.denominator}"

    @property
    def beats_per_measure(self) -> int:
        """Get number of beats per measure."""
        return self.numerator

    @property
    def beat_unit(self) -> int:
        """Get the note value that represents one beat."""
        return self.denominator

    @property
    def is_compound(self) -> bool:
        """Check if this is a compound meter (divisible by 3)."""
        return self.numerator % 3 == 0 and self.numerator > 3

    @property
    def is_simple(self) -> bool:
        """Check if this is a simple meter (not compound)."""
        return not self.is_compound

    @property
    def feel(self) -> str:
        """Get the rhythmic feel of this time signature."""
        if self.numerator == 4:
            return "four-on-the-floor"
        elif self.numerator == 3:
            return "waltz"
        elif self.numerator == 5:
            return "asymmetric"
        elif self.numerator == 7:
            return "complex-asymmetric"
        elif self.is_compound:
            return "compound"
        else:
            return "irregular"

    def get_accent_pattern(self) -> list[int]:
        """Get typical accent pattern for this time signature.

        Returns:
            List of beat indices (0-indexed) that should be accented
        """
        if self.numerator == 4:
            return [0, 2]  # Strong on 1 and 3
        elif self.numerator == 3:
            return [0]  # Strong on 1
        elif self.numerator == 5:
            # Common grouping: 3+2 or 2+3
            return [0, 3]  # Accent on 1 and 4
        elif self.numerator == 7:
            # Common grouping: 2+2+3
            return [0, 2, 4]  # Accent on 1, 3, and 5
        elif self.numerator == 6:
            if self.denominator == 8:
                return [0, 3]  # Compound duple: 2 groups of 3
            else:
                return [0, 3]  # Simple: accent on 1 and 4
        else:
            # Default: accent on first beat
            return [0]

    def __str__(self) -> str:
        return self.name


# Common time signatures
COMMON_TIME_SIGNATURES = {
    "4/4": TimeSignature(4, 4, "4/4 (Common Time)"),
    "3/4": TimeSignature(3, 4, "3/4 (Waltz)"),
    "5/4": TimeSignature(5, 4, "5/4 (Irregular)"),
    "7/4": TimeSignature(7, 4, "7/4 (Complex)"),
    "6/8": TimeSignature(6, 8, "6/8 (Compound)"),
    "7/8": TimeSignature(7, 8, "7/8 (Balkan)"),
    "9/8": TimeSignature(9, 8, "9/8 (Compound Triple)"),
}


def parse_time_signature(signature_str: str) -> TimeSignature:
    """Parse a time signature string like '3/4' or '5/4'.

    Args:
        signature_str: Time signature in format "numerator/denominator"

    Returns:
        TimeSignature object

    Raises:
        ValueError: If format is invalid
    """
    if signature_str in COMMON_TIME_SIGNATURES:
        return COMMON_TIME_SIGNATURES[signature_str]

    try:
        parts = signature_str.split("/")
        if len(parts) != 2:
            raise ValueError(f"Invalid time signature format: {signature_str}")

        numerator = int(parts[0])
        denominator = int(parts[1])

        # Validate
        if numerator < 1 or numerator > 16:
            raise ValueError(f"Numerator must be between 1 and 16: {numerator}")

        if denominator not in [2, 4, 8, 16]:
            raise ValueError(f"Denominator must be 2, 4, 8, or 16: {denominator}")

        return TimeSignature(numerator, denominator)

    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid time signature: {signature_str}. Format should be 'N/D' (e.g., '4/4')") from e


def get_available_time_signatures() -> list[str]:
    """Get list of available time signature names."""
    return list(COMMON_TIME_SIGNATURES.keys())
