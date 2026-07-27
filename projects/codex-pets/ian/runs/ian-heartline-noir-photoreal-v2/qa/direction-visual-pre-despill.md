# Pre-despill direction review

- Cardinal revision 4 is the approved direction ground: `000` visibly looks upward; `090` is a right-facing profile with the nose toward the viewer's screen-right; `180` visibly looks downward; `270` is the opposite left-facing profile.
- Both look rows were completely regenerated from that cardinal ground after blind evidence showed the prior horizontal directions were inverted. Rejected cardinal and row sources are preserved in `sources/` and indexed by the job manifest.
- The visual direction sheet keeps Ian's face, outfit, scale, boots, and baseline coherent. The row-9 right-hand arc and row-10 left-hand arc now follow the approved opposite profile families.
- Continuity measurement still flags profile-transition area/diff changes for the root final-QA review; no deterministic clipping, alpha-hole, or registration failure was found.
- This is pre-despill only. Structure validation passes when chroma-edge warnings are allowed; strict chroma cleanup belongs to the root-owned final despill step.
