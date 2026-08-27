"""Deterministic cyber risk quantification functions."""

from .eal import calculate_asset_risks, calculate_eal, calculate_impact, calculate_likelihood

__all__ = [
    "calculate_asset_risks",
    "calculate_eal",
    "calculate_impact",
    "calculate_likelihood",
]