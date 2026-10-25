#!/usr/bin/env python3
"""Illustrative tunnel traffic-wind energy and incident-review simulator.

This standard-library demonstration does not read a camera, run an AI model,
send network alerts, or control a tunnel device. Numbers are assumptions, not
measurements or a design recommendation.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Assumptions:
    turbines: int = 8
    vehicles_per_day: int = 1000
    air_speed_m_s: float = 6.0
    pulse_seconds_per_vehicle: float = 10.0
    swept_area_m2: float = 0.25
    air_density_kg_m3: float = 1.2
    power_coefficient: float = 0.25
    generator_efficiency: float = 0.75
    converter_efficiency: float = 0.90
    led_w: float = 12.0
    led_h_per_day: float = 4.0
    camera_w: float = 5.0
    edge_compute_w: float = 8.0


def calculate(a: Assumptions) -> dict[str, object]:
    air_power_w = (
        0.5 * a.air_density_kg_m3 * a.swept_area_m2 * a.air_speed_m_s**3
    )
    dc_power_per_turbine_w = (
        air_power_w
        * a.power_coefficient
        * a.generator_efficiency
        * a.converter_efficiency
    )
    wh_per_vehicle_per_turbine = (
        dc_power_per_turbine_w * a.pulse_seconds_per_vehicle / 3600.0
    )
    gross_array_wh_day = (
        wh_per_vehicle_per_turbine * a.vehicles_per_day * a.turbines
    )

    led_wh_day = a.led_w * a.led_h_per_day
    camera_wh_day = a.camera_w * 24.0
    edge_wh_day = a.edge_compute_w * 24.0
    total_load_wh_day = led_wh_day + camera_wh_day + edge_wh_day

    return {
        "status": "illustrative assumptions; not measured tunnel output",
        "assumptions": asdict(a),
        "turbine_estimate": {
            "air_power_per_turbine_during_pulse_w": round(air_power_w, 4),
            "dc_output_per_turbine_during_pulse_w": round(
                dc_power_per_turbine_w, 4
            ),
            "energy_per_vehicle_per_turbine_wh": round(
                wh_per_vehicle_per_turbine, 6
            ),
            "gross_array_energy_wh_per_day": round(gross_array_wh_day, 3),
        },
        "example_load_wh_per_day": {
            "supplementary_led": round(led_wh_day, 3),
            "camera": round(camera_wh_day, 3),
            "edge_compute": round(edge_wh_day, 3),
            "total": round(total_load_wh_day, 3),
            "gross_energy_fraction_before_losses": round(
                gross_array_wh_day / total_load_wh_day
                if total_load_wh_day
                else 0.0,
                4,
            ),
        },
        "not_included": [
            "measured tunnel velocity time series",
            "battery, wiring, standby, and downtime losses",
            "turbine interaction and ventilation effects",
            "incremental vehicle propulsion energy",
            "safety margin or emergency-power sizing",
        ],
    }


def synthetic_incident_review() -> dict[str, object]:
    """Return a fake review item; it does not represent real sensor inference."""
    return {
        "synthetic_demo_only": True,
        "event_type": "possible_vehicle_incident_with_smoke_cue",
        "tunnel_zone": "DEMO-ZONE-01",
        "camera": "DEMO-CAMERA-01",
        "timestamp": "2026-10-25T12:00:00Z (synthetic)",
        "review_state": "candidate_pending_operator_review",
        "actions": {
            "dispatch_sent": False,
            "fan_or_smoke_control_command_sent": False,
            "water_suppression_command_sent": False,
            "next_step": (
                "Tunnel operator review and approved emergency procedure"
            ),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--turbines", type=int, default=8)
    parser.add_argument("--vehicles-per-day", type=int, default=1000)
    parser.add_argument("--air-speed", type=float, default=6.0, help="m/s")
    parser.add_argument("--pulse-seconds", type=float, default=10.0)
    parser.add_argument("--area", type=float, default=0.25, help="m^2 per turbine")
    parser.add_argument("--cp", type=float, default=0.25, help="assumed turbine coefficient")
    parser.add_argument("--generator-efficiency", type=float, default=0.75)
    parser.add_argument("--converter-efficiency", type=float, default=0.90)
    parser.add_argument("--led-w", type=float, default=12.0)
    parser.add_argument("--led-hours", type=float, default=4.0)
    parser.add_argument("--camera-w", type=float, default=5.0)
    parser.add_argument("--edge-compute-w", type=float, default=8.0)
    parser.add_argument("--demo-incident", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.turbines < 1 or args.vehicles_per_day < 0:
        raise SystemExit("turbines must be >= 1 and vehicles-per-day must be >= 0")
    if min(args.air_speed, args.pulse_seconds, args.area) < 0:
        raise SystemExit("air speed, pulse duration, and area cannot be negative")
    if not 0.0 <= args.cp <= 1.0:
        raise SystemExit("cp must be between 0 and 1")
    if not 0.0 <= args.generator_efficiency <= 1.0:
        raise SystemExit("generator efficiency must be between 0 and 1")
    if not 0.0 <= args.converter_efficiency <= 1.0:
        raise SystemExit("converter efficiency must be between 0 and 1")
    if min(args.led_w, args.led_hours, args.camera_w, args.edge_compute_w) < 0:
        raise SystemExit("load powers and operating hours cannot be negative")

    assumptions = Assumptions(
        turbines=args.turbines,
        vehicles_per_day=args.vehicles_per_day,
        air_speed_m_s=args.air_speed,
        pulse_seconds_per_vehicle=args.pulse_seconds,
        swept_area_m2=args.area,
        power_coefficient=args.cp,
        generator_efficiency=args.generator_efficiency,
        converter_efficiency=args.converter_efficiency,
        led_w=args.led_w,
        led_h_per_day=args.led_hours,
        camera_w=args.camera_w,
        edge_compute_w=args.edge_compute_w,
    )
    result: dict[str, object] = calculate(assumptions)
    if args.demo_incident:
        result["synthetic_incident_review"] = synthetic_incident_review()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
