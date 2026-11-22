### Selftest: 4 of 4 areas passed

| | |
| --- | --- |
| SolidWorks | 33.1.2 (year 2025), english |
| Templates | part: ai_concept_part_standard_planes.prtdot; assembly: Assembly.asmdot; drawing: Drawing.drwdot |
| OS | Windows-10-10.0.19045-SP0 |
| Python | 3.13.4, pywin32 312 |
| solidworks-mcp-python | 2.0.0 |

#### part: PASS

| Check | Expected | Measured | Tolerance | Result |
| --- | --- | --- | --- | --- |
| block: volume_mm3 | 8,000.00 mm3 | 8,000.00 | 0.01 % | pass |
| block: bounding_box_mm | [40.00, 10.00, 20.00] mm | [40.00, 10.00, 20.00] | 0.01 mm | pass |
| after the hole: volume_mm3 | 7,214.60 mm3 | 7,214.60 | 0.01 % | pass |
| after the hole: bounding_box_mm | [40.00, 10.00, 20.00] mm | [40.00, 10.00, 20.00] | 0.01 mm | pass |
| after the fillet: volume_mm3 | 7,180.27 mm3 | 7,180.27 | 0.01 % | pass |
| after the fillet: bounding_box_mm | [40.00, 10.00, 20.00] mm | [40.00, 10.00, 20.00] | 0.01 mm | pass |
| pin: volume_mm3 | 1,417.64 mm3 | 1,417.64 | 0.01 % | pass |
| pin: bounding_box_mm | [9.50, 20.00, 9.50] mm | [9.50, 20.00, 9.50] | 0.01 mm | pass |

Tools: `create_part` x2, `create_sketch` x3, `add_rectangle`, `exit_sketch` x3, `create_extrusion` x2, `verify_model` x4, `add_circle` x2, `create_cut_extrude`, `add_fillet`, `save_as` x2

#### assembly: PASS

| Check | Expected | Measured | Tolerance | Result |
| --- | --- | --- | --- | --- |
| assembly: component_count | 2 components | 2 | exact | pass |
| assembly: mate_count | 2 mates | 2 | exact | pass |
| assembly: no_interference | yes | yes | - | pass |

Tools: `create_assembly`, `insert_component` x2, `list_components`, `add_mate` x2, `verify_model`

#### drawing: PASS

| Check | Expected | Measured | Tolerance | Result |
| --- | --- | --- | --- | --- |
| drawing: view_count | 1 view | 1 | exact | pass |

Tools: `create_drawing`, `add_drawing_view`, `list_drawing_views`

#### export: PASS

| Check | Expected | Measured | Tolerance | Result |
| --- | --- | --- | --- | --- |
| export: step_file_bytes | > 0 bytes | 23742 | - | pass |

Tools: `activate_document`, `export_step`
