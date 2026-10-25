# Tunnel Traffic-Wind Lighting and Incident-Response Demonstrator

**A standalone road-tunnel research concept.** This project examines whether guarded microturbines exposed to vehicle-induced tunnel airflow can contribute to a supplementary low-voltage lighting bus, while an independent AI-assisted monitoring concept raises candidate incident alerts for a tunnel operator.

This repository is independent of any street-lamp project. It concerns only a tunnel installation.

> **Safety and evidence status:** Research concept and executable simulation only. No tunnel measurements, prototype performance, certified AI model, emergency dispatch integration, fire suppression control, or fan control are provided. The turbine output is not free energy: vehicle propulsion contributes to the airflow, and a turbine may increase flow resistance. Do not connect this demonstrator to tunnel equipment or emergency services.

## Abstract

Road tunnels have continuous lighting, monitoring, and ventilation requirements, while traffic passage creates transient wakes and a tunnel piston effect. This project proposes measuring those airflow events and testing whether compact, guarded turbines can produce useful electricity for a defined supplementary lighting load. A metered low-voltage bus could also contribute to non-critical monitoring loads after site-specific measurement. The repository provides a transparent energy model, an illustrative load budget, a low-voltage block diagram, materials and connection guidance, and a runnable Python scenario simulator.

The safety concept keeps required lighting and all approved fire, smoke-control, communications, and control-room systems on their existing engineered supplies. AI output is a candidate event for operator review. It does not directly call an ambulance, hospital, or police station; change fan speed; or activate water suppression. Tunnel smoke-control decisions depend on tunnel geometry, traffic state, ventilation design, incident location, and emergency procedures. Actual systems require tunnel-owner approval, qualified fire/life-safety and electrical engineers, validated equipment, and jurisdiction-specific acceptance.

## What is in this repository

- [Research concept and sample calculations](docs/RESEARCH.md)
- [Materials, connection schedule, and circuit block diagram](docs/HARDWARE.md)
- [AI event workflow, alert handoff, and safety boundaries](docs/AI_AND_SAFETY.md)
- [Runnable energy and incident scenario simulator](src/tunnel_demo.py)

## Illustrative calculation

The default simulator scenario uses **assumed** values, not tunnel measurements: eight identical turbines, swept area 0.25 m² each, 6 m/s airflow for 10 seconds per vehicle, 1,000 vehicles/day, turbine power coefficient 0.25, generator efficiency 0.75, and converter efficiency 0.90. The model estimates about **5.47 W per turbine during the assumed gust**, **15.19 Wh/day per turbine**, and **121.5 Wh/day gross for the eight-turbine array**.

The example load is 12 W of supplementary LED lighting for 4 h/day (48 Wh/day), a 5 W camera for 24 h/day (120 Wh/day), and an 8 W edge-compute unit for 24 h/day (192 Wh/day): **360 Wh/day total**. The assumed array output is about 34% of that load before storage, standby, wiring, and vehicle-energy effects. It is not a prediction or a guarantee. The model does not know the tunnel's real velocity time series or the additional propulsion energy caused by turbine drag, so it cannot claim net energy savings.

Run the calculation; the same default result is saved in [examples/demo_output.json](examples/demo_output.json):

~~~sh
python src/tunnel_demo.py
~~~

Run a synthetic incident/fire workflow example (prints a review item only):

~~~sh
python src/tunnel_demo.py --demo-incident
~~~

The program uses only the Python standard library. Adjust assumptions with --turbines, --vehicles-per-day, --air-speed, --pulse-seconds, --area, --cp, --generator-efficiency, --converter-efficiency, --led-w, --led-hours, --camera-w, and --edge-compute-w. Its synthetic event is not an AI model result and it has no network, dispatch, PLC, fan, pump, or actuator interface.

## System boundary

~~~mermaid
flowchart LR
  V[Passing vehicles] -->|transient airflow| T[Guarded turbine array]
  T --> R[Rectifier and wind charge controller]
  R --> B[Protected storage and metered low-voltage DC bus]
  B --> L[Supplementary LED branch]
  B --> M[Non-critical monitor branch, only if measured surplus exists]
  C[Camera and edge inference] --> E[Candidate event with timestamp and location]
  E --> O[Control-room review]
  O -->|approved emergency procedure| S[Authorized responders]
  F[Independent approved fire detection] --> P[Certified tunnel safety PLC / operator]
  P --> X[Pre-engineered smoke-control and suppression systems]
  G[Existing approved utility / UPS / emergency supply] --> Q[Required lighting, safety systems, and control room]
~~~

The harvested-energy branch is supplementary. It does not replace the tunnel's required power, lighting, fire alarm, smoke-control, or emergency communications systems. The AI path has no direct connection to those safety-critical outputs.

## Research basis

Published work has prototyped turbines for vehicle-induced airflow in road tunnels and experimentally examined turbines in passing-vehicle gusts. Those studies support site-specific testing; they do not establish the output of this proposed array. PIARC guidance describes automatic incident detection as an input to a control-room workflow and emphasizes that smoke-control actions depend on the tunnel and emergency strategy. See the sources in [docs/RESEARCH.md](docs/RESEARCH.md).

## Project status

- **Included:** conceptual architecture, assumptions, hand-checkable sample calculation, materials shortlist, generic low-voltage connection diagram, and safe simulation.
- **Not included:** engineered tunnel drawings, structural attachments, certified battery/charger selection, full-size wiring design, real AI weights or incident dataset, dispatch contacts, PLC logic, pump or fan control, or measured results.
- **Before any pilot:** agree the research plan with the tunnel owner; characterize traffic and airflow; assess turbine blockage, noise, vibration, debris, fire, and maintenance; complete the lighting and fire/smoke safety case; and validate the incident workflow with the responsible agencies.

## References

See the numbered references in [docs/RESEARCH.md](docs/RESEARCH.md). Key sources include the road-tunnel turbine prototype by Gallorini and Barelli, the passing-vehicle turbine experiments by Łyskawiński et al., CIE tunnel-lighting guidance, and PIARC's Road Tunnels Manual.
