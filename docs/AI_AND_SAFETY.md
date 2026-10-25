# AI Event Review, Alerts, Fire Response, and Safety Boundaries

## 1. Intended software role

The software in this repository is a local simulation. It demonstrates energy arithmetic and the shape of a candidate incident-review message. It has no camera capture, AI weights, network requests, dispatch API, PLC connection, relay output, fan command, water valve command, or emergency-system connection.

In a future research implementation, video analytics could identify candidate stopped vehicles, collisions, smoke, or flames. Such a model is not proof that an incident occurred. A detection pipeline needs tunnel-specific training and validation data, event aggregation over time, confidence calibration, duplicate suppression, camera/zone/time metadata, and a human review procedure. Fire detection must also use the tunnel's approved fire-detection equipment; camera analytics are an additional input, not a replacement.

PIARC describes automatic incident detection as a source of alarms and information for the tunnel operator. It notes that different devices provide different levels of information and may need operator verification. This supports a candidate-event workflow with control-room review instead of an AI-to-dispatch shortcut.

## 2. Candidate alert record

A future system may create a record with fields such as:

~~~json
{
  "event_id": "generated-unique-id",
  "event_type": "possible_vehicle_incident",
  "tunnel_id": "operator-assigned-id",
  "zone_id": "operator-assigned-zone",
  "camera_id": "operator-assigned-camera",
  "timestamp_utc": "ISO-8601 timestamp from synchronized clock",
  "model_version": "validated model identifier",
  "score": "calibrated score or null",
  "evidence_reference": "access-controlled video clip identifier",
  "independent_fire_alarm": "not provided / active / clear",
  "review_state": "candidate_pending_operator_review"
}
~~~

Do not store public responder telephone numbers in source code or automatically infer an ambulance, hospital, or police destination. The tunnel operator's approved control room and emergency plan define who is called, by whom, and through which authorized communications system. The demonstration's incident output is synthetic and sends nothing.

## 3. Fire, water suppression, and smoke-control response

There is no universal safe rule to “run exhaust fans faster” after an AI sees flames. Ventilation direction and speed influence smoke spread, stratification, evacuation tenability, downstream traffic, escape routes, and firefighter access. PIARC guidance says the ventilation strategy and emergency response depend on the tunnel configuration and the operational incident plan; during the firefighting phase, ventilation operation is a decision for incident command in coordination with the system's approved capabilities.

Likewise, a fixed water-based firefighting system must be integrated with tunnel fire engineering, detection, water supply, drainage, electrical resilience, maintenance, and emergency-service procedures. The demonstrator does not activate sprinklers, deluge, mist, pumps, dampers, or fans. A real control sequence must come from the approved tunnel safety case and be implemented only in certified equipment by the responsible integrator.

## 4. Human-reviewed escalation concept

1. Vision or sensor analytics emit a time- and zone-stamped candidate.
2. The system preserves an access-controlled evidence reference and system health state.
3. The tunnel control room reviews CCTV and independent sensors.
4. The authorized operator follows the tunnel's incident plan: traffic control, public warnings, evacuation guidance, and responder notifications.
5. Approved fire detection and safety controls operate under their validated sequences and incident-command procedures.
6. The event and operator decisions are logged for review and system improvement.

This describes a workflow, not an implementation or authorization to contact emergency services.

## 5. Validation before operational use

At minimum, a future study must define the tunnel and operating context; obtain privacy and data-use approvals; create labeled examples across traffic, lighting, smoke, occlusion, camera failures, and normal congestion; split evaluation by recording session or site; and report event-level precision, recall, false alarms per camera-hour, missed-event categories, latency, camera availability, and operator workload. Acceptance limits must be set by the tunnel owner and applicable requirements before live alerts.

The full system safety case must consider power loss, loss of communications, false alarms, missed fires, clock drift, sensor disagreement, cybersecurity, manual override, maintenance isolation, and interactions among ventilation, lighting, fire protection, and evacuation. The edge AI and harvested-energy demonstrator must fail without impairing approved tunnel systems.

## 6. Safety references

- PIARC, [Monitoring/Incident detection](https://tunnelsmanual.piarc.org/en/equipment-systems/monitoringincident-detection).
- PIARC, [Automatic incident detection](https://tunnelsmanual.piarc.org/en/equipment-systems-monitoringincident-detection/automatic-incident-detection).
- PIARC, [Fire detection systems](https://tunnelsmanual.piarc.org/en/equipment-systems-monitoringincident-detection/fire-detection-systems).
- PIARC, [Operational tasks](https://tunnelsmanual.piarc.org/en/operation-and-maintenance-operation/operational-tasks).
- PIARC, [Ventilation strategies](https://tunnelsmanual.piarc.org/en/operation-and-maintenance-operation/ventilation-strategies) and [Tunnel ventilation systems](https://tunnelsmanual.piarc.org/en/equipment-systems-mitigation-fire-hazards/tunnel-ventilation-systems).
- CIE, [Guide for the Lighting of Road Tunnels and Underpasses](https://www.cie.co.at/publications/guide-lighting-road-tunnels-and-underpasses-2nd-ed).
