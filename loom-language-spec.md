# Loom Language Specification
## Design Draft v0.2

**Author:** Tom Munnecke  
**Status:** Design exploration — not yet implemented  
**Preceded by:** ["Loom of the Future" (Google Doc, 2024)](https://docs.google.com/document/d/1Ymrs-lmFv8VuhLzFcnmbkBVeKNZIO8Z6nhF9sBaU4uw)  
**Related:** "Formalizing physics terms with Lean dependency trees" (separate session)

---

## 1. Purpose

Loom is a language for describing *knowledge tapestries* — networks of fundamental patterns ("intrinsics") and the cascades they produce across scales. It is designed to:

- Make cross-domain transfer of knowledge expressible and verifiable
- Support both informal human reasoning and formal machine verification
- Quote [[Lean theorem prover|Lean]] as a sublanguage for formal grounding of specific claims
- Capture "wrinkles" (inconsistencies, soft laws, contested zones) as first-class citizens
- Model accountability and governance structures, not just content

Loom replaces the L-system string-rewriting approach of v0.01 with a typed graph model. L-systems are elegant but too low-level — they generate strings rather than *meaning*, and they have no native notion of scale, context, confidence, or verification.

---

## 2. Core Model

### 2.1 Intrinsics

An **intrinsic** is a fundamental pattern, property, or relationship that manifests across multiple scales. Examples: cooperation, resilience, trust, scarcity, dual-use.

Intrinsics are not simply labels — they have:
- A **scale profile**: which levels (individual → community → civilization) they apply at
- An optional **Lean type signature** for formal grounding
- A **texture**: how well-understood / contested the intrinsic is (smooth, wrinkled, rugged, torn — from the source document)

### 2.2 Cascades

A **cascade** is a directed relationship between intrinsics: "when A is present at scale S, it tends to produce B at scale S'." Cascades can be:
- **Hard** (law-like, inviolable — Scott Clark: "physical laws as unit tests")
- **Soft** (statistical tendencies — Simeon Bird: "laws that are often true vs laws that cannot be broken")
- **Contextual** (behavior depends on declared context)

### 2.3 Scales

Scales form a partially ordered set. Default scale hierarchy for social systems:

```
sub-cellular → individual → family → community → institution → civilization → planetary
```

For physical systems:

```
quantum → molecular → mesoscale → macroscale → astrophysical
```

Loom does not hard-code a scale hierarchy; they are declared per-domain. Simeon Bird's point that AI discovers symmetries that allow compression across scales is captured by `scale-invariant` annotations.

### 2.4 Contexts

A **context** is a named frame that conditions cascade behavior. David Brin identifies three missing contexts in AI discourse: biological, ecological, and governance. Contexts are first-class in Loom — you declare them and cascade rules are context-sensitive.

### 2.5 Confidence and Discovery

Barry Barish's closing challenge — "we have no five-sigma equivalent for AI-assisted discovery" — is addressed by making **confidence** a required annotation on soft laws. Loom does not solve this problem, but it forces the question to be asked.

---

## 3. Syntax

### 3.1 Intrinsic Declarations

```loom
-- Simple intrinsic
intrinsic Cooperation

-- With scale profile
intrinsic Cooperation
  scales [individual, family, community, institution, civilization]

-- With Lean type for formal grounding (quotation syntax: lean⟨ ... ⟩)
intrinsic Force
  lean⟨
    structure Force where
      agent₁  : Agent
      agent₂  : Agent
      benefit : Benefit
  ⟩

-- Physics intrinsic, grounded in Lean dependency tree
intrinsic KineticEnergy
  scales [molecular, macroscale]
  lean⟨
    def KineticEnergy (m : Mass) (v : Velocity) : Energy :=
      (1/2 : ℝ) * m.val * v.val ^ 2
  ⟩
```

### 3.2 Cascade Declarations

```loom
-- Soft cascade: a tendency, not a law
cascade Cooperation → Health
  at scale: individual
  strength: soft
  evidence: "Salk epidemic-of-health model"

-- Hard cascade: physically inviolable (provable in Lean)
cascade Force → Acceleration
  at scale: macroscale
  strength: hard
  lean⟨ theorem newton_second (f : Force) (m : Mass) :
          Acceleration := f.magnitude / m.val ⟩

-- Contextual cascade: behavior differs by context
cascade Cooperation → Trust
  in context: LowScarcity   -- holds
  in context: HighScarcity  -- may not hold (contested)
  strength: soft
  confidence: sigma 2.1     -- Barish: explicit about epistemic status

-- Cross-scale cascade
cascade Cooperation@individual → Cooperation@community
  mechanism: "social contagion"
  scale-invariant: true     -- Bird: symmetry across scales
```

### 3.3 Laws

Laws constrain the space of possible cascades.

```loom
-- Hard law: must not be violated (Clark: "laws of physics as unit tests")
law [hard] Conservation_of_Energy :
  ∀ system : PhysicalSystem, system.total_energy = const
  lean⟨ theorem energy_conservation ... ⟩

-- Soft law: statistical tendency, must carry confidence annotation (Barish)
law [soft, confidence: sigma 3.5] Cooperation_precedes_Trust :
  usually Cooperation → Trust
  in context: OpenGovernance
  counterexamples: [PrisonersDilemma]

-- Scale invariance law (Bird)
law [scale-invariant] CooperationSymmetry :
  ∀ s₁ s₂ : Scale, Cooperation@s₁ ≅ Cooperation@s₂
  -- "every part of the universe should be in some sense the same"
```

### 3.4 Context Declarations

```loom
-- Brin's "missing contexts"
context BiologicalContext where
  computation_substrate : Biological | Digital | Hybrid
  energy_budget         : Watts
  -- seven-watt brain observation: biological intelligence runs on 7W
  reference             : BrinSIR2026

context EcologicalContext where
  ecosystem_type        : NaturalBiosphere | DigitalBiosphere | Hybrid
  evolutionary_pressure : ReproductionReward
  -- Brin: we are creating a new ecosystem subject to evolutionary pressures
  agent_types           : List (Agent, RewardStructure)

context GovernanceContext where
  model : Enlightenment | Feudal | Chaos | Skynet
  -- Brin: only Enlightenment is self-consistent
  accountability : Reciprocal | Hierarchical | None
  transparency   : Open | Closed
```

### 3.5 Accountability Structures (Brin)

```loom
-- The Enlightenment model: reciprocal accountability through adversarial transparency
accountability EnlightenmentModel where
  mechanism : AdversarialTransparency
  -- "when attacked by a predatory language-manipulation system called a lawyer,
  --  you hire your own" — Brin 2026
  actors    : Reciprocally_accountable_free_citizens
  tattletale_advantage : true
  -- good-dog agents gain evolutionary advantage by exposing bad actors

actor TattletaleAgent : AIAgent where
  observes     : List (Action, Context)
  reports_to   : AccountabilityStructure
  reward_type  : ReputationGain ++ ReproductiveAdvantage
  -- Brin: substitute ego (external watch) for superego (conscience)
```

### 3.6 Wrinkles and Tapestry Texture

```loom
-- Wrinkle: a place where the tapestry is inconsistent or contested
wrinkle HealthcareFragmentation where
  description     : "medicine organized by body part, not by patient"
  tension_between : [Specialization, Holism, PatientContinuity]
  cause           : FeeForServiceIncentives
  resolution      : IntegratedCareTapestry
  texture         : Torn  -- from the source doc taxonomy

-- Tapestry texture vocabulary (from source doc):
-- Smooth    : well-integrated, consensus reached
-- Textured  : diverse, multifaceted, rich
-- Wrinkled  : inconsistencies, gaps, competing claims
-- Rugged    : entrenched conflict, local optima (Bird: evolutionary valleys)
-- Glossy    : dangerously oversimplified, panglossian
-- Torn      : breakdown of communication, suppression

-- Tao: proof indigestion — a wrinkle in mathematical infrastructure
wrinkle ProofIndigestion where
  description : "AI generates proofs faster than humans can verify or digest them"
  tension_between : [AIGeneration, HumanVerification, InfrastructureCapacity]
  texture     : Wrinkled
  resolution  : NewInfrastructure  -- Tao's SAIR competitions / Lean tooling
```

### 3.7 Transfer Learning Declarations

```loom
-- Declare that an intrinsic pattern discovered in one domain transfers
transfer CozyNook
  from : ArchitecturalDesign
  to   : [WorkplaceDesign, AIInterfaceDesign, MentalHealthTherapy]
  mechanism : IntrinsicResonance
  -- "intrinsic resonance" — shared emotional/psychological quality
  -- not a hyperlink (explicit), but a deeper structural similarity
  confidence : soft

transfer PandemicResponse_to_ClimatePolicy
  from : COVID19Pandemic
  to   : ClimateChange
  transferable_intrinsics : [Cooperation, Trust, Inequality, Innovation, Fear]
  lesson : "cooperation + innovation cascade is faster when trust is high"
  evidence : mRNAVaccineTimeline
```

### 3.8 Discovery Confidence (Barish)

```loom
-- Every discovery claim must carry an epistemic status
discovery NeutrinoMassLowerBound where
  method     : AI_assisted_field_level_inference  -- Woo 2026
  confidence : sigma 4.2
  -- Barish: no five-sigma equivalent for AI yet; must be explicit
  validation : [Simulation_to_real_gap_addressed, PhysicalLawsAreUnitTests]
  open_question : "AI scores are overoptimistic — correction method TBD"
```

---

## 4. Lean Sublanguage Integration

Lean quotations appear inside `lean⟨ ... ⟩` blocks anywhere in a Loom document. The relationship is:

| Loom | Lean |
|------|------|
| `intrinsic Foo` | `structure Foo` or `def Foo : Type` |
| `law [hard] ...` | `theorem ...` with a proof |
| `cascade A → B` (hard) | `def cascade_AB : A → B` |
| `law [soft]` | No Lean proof required; carries sigma annotation instead |
| `context C where` | `namespace C` or `structure C` |

The key design principle: **Lean handles what can be formally verified; Loom handles the rest.** Soft laws, contested wrinkles, ecological contexts, and accountability structures live in Loom. Hard laws, type signatures, and provable cascades are grounded in Lean.

This is analogous to how Simeon Bird's panel described surrogate models: Lean is the "high-fidelity simulation" for specific claims; Loom is the "emulator" for navigating the larger landscape.

---

## 5. Feature Inventory from the Summit

| Feature | Suggested by | Status |
|---------|-------------|--------|
| Hard vs soft laws | Scott Clark: "physical laws as unit tests" | Designed (§3.3) |
| Scale annotations | Simeon Bird: "scale-invariant properties" | Designed (§3.1) |
| Symmetry-based compression | Bird: "use symmetries to decide what to throw away" | Partial — `scale-invariant` flag |
| Contextual cascades | David Brin: three missing contexts | Designed (§3.4) |
| Accountability actors | Brin: Enlightenment / tattletale mechanism | Designed (§3.5) |
| Discovery confidence | Barry Barish: five-sigma equivalent | Partial — `confidence: sigma N` |
| Wrinkle declarations | Source doc + Tao: proof indigestion | Designed (§3.6) |
| Lean quotation | Tao: Lean theorem prover; Lean dependency tree chat | Designed (§4) |
| Transfer learning | Source doc + COVID case study | Designed (§3.7) |
| Objective function specification | Clark: "knowing what you're optimizing is the hardest part" | Not yet designed |
| Simulation-to-real gap | Bian: "fundamental inconsistency in AI on real data" | Not yet designed |
| Proof indigestion / infrastructure | Tao: journals can't absorb AI output | Modeled as a wrinkle; needs more |
| Multi-fidelity levels | Clark: "surrogate good enough to decide next step" | Not yet designed |

---

## 6. What Loom Is Not

- **Not a general programming language.** Loom describes knowledge structures, not computation. Lean handles computation and proof.
- **Not an ontology language.** Loom is intentionally less formal than OWL/RDF. Intrinsics are patterns, not rigid class hierarchies.
- **Not a replacement for natural language.** Loom documents are meant to coexist with prose — they formalize the skeleton, not the flesh.
- **Not L-systems.** The string-rewriting heritage of v0.01 is abandoned. Cascades are typed edges in a graph, not string productions.

---

## 7. Personal Background: The Language Architect Perspective

The Loom Language continues a trajectory that includes:

- **MUMPS** (Massachusetts General Hospital Utility Multi-Programming System): 19 functions, 22 commands → backbone of VA VistA EHR, foundation for Epic Systems. The lesson: extreme economy of primitives, combined with integrated data capabilities, can achieve outsized reach.
- **Pattern Language** (Christopher Alexander): each pattern names a recurring problem, its solution, and the rationale. Loom intrinsics are pattern-language patterns with formal Lean typing.
- **Vernor Vinge's technological singularity**: the dedication of the source book. Vinge's insight was that context matters more than raw capability — the same point Brin made in 2026.

---

## 8. Open Questions

1. **Grammar**: What is the full BNF grammar? The syntax sketched above is illustrative, not complete.
2. **Lean quotation semantics**: How are Lean types extracted from quotations for type-checking? Does Loom run a Lean elaborator, or is quotation purely syntactic?
3. **Scale lattice**: Is the scale ordering a total order, partial order, or something richer (e.g., can individual and institution be incomparable)?
4. **Confidence calculus**: When soft cascades compose, how do confidence levels propagate? (This is Barish's unsolved problem restated for cascade chains.)
5. **Tooling**: A Loom interpreter/visualizer would show the tapestry as a graph with texture annotations. What is the right representation?
6. **The objective function problem** (Clark): Loom currently describes *what* cascades, not *what we are optimizing for*. A `goal` or `objective` declaration is needed.
7. **Wrinkle resolution protocol**: How does a wrinkle get resolved into a smooth tapestry? This is the governance / Enlightenment problem.

---

## 9. Relation to the Source Document

The "Loom of the Future" Google Doc (2024) contains the conceptual foundations. What is worth preserving:

| From source doc | Status in this spec |
|----------------|---------------------|
| Weaver paradigm vs Gutenberg | Background; motivates the language |
| Intrinsics concept | Core (§2.1) |
| L-system production rules | **Replaced** by typed cascade graph |
| Tapestry texture vocabulary (smooth/wrinkled/etc.) | Preserved (§3.6) |
| Scale-free design / cascades | Core (§2.2, §2.3) |
| Transfer learning | Core (§3.7) |
| Abundant civilization | Background vision |
| DKN / AHN health architecture | Application domain, not language spec |
| Dysidentity as negative intrinsic | Example application |
| Python Loom interpreter | Superseded by this design |
| Loom .01 Reference Manual | Superseded by this spec |

---

*This document is a design exploration. Implementation details, parser grammar, and Lean integration require further development.*
