# preflight_must_run_gate_criteria

A preflight pipeline that passes internal stages but doesn't exercise the actual gate test gives false confidence. Fitness dropped 0.5→0 despite all stages passing — the pipeline verified the wrong thing. Preflight must run or replicate the real gate test criteria, not just its own checklist.
