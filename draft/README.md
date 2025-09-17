# Salmon Stream Inspection Ontology (SSIO) — Snapshot

This repository contains three Turtle files:
- `draft_environment_information.ttl` — Environmental features (water bodies, conditions, impacts, regions, identifiers).
- `draft_salmon_information.ttl` — Salmon observations (life stages, predators, species, salmon→impact link).
- `draft_inspection_information.ttl` — Inspection details, methods (ground/aerial), SSN/SOSA alignment, method metadata.

---

## 1) Current class → subclass snapshot

### Environmental
- Environmental  
  - Water Body Types  
    - LenticWaterBody → Lake, Pond  
    - LoticWaterBody → Creek, Stream, River, Slough  
    - Estuary  
  - StreamCondition  
    - WaterFlow → HighFlow, LowFlow  
    - StreamObstruction  
      - ObstructionPassability → Passable, Impassable  
      - ObstructionOrigin → NaturalObstruction, ArtificialObstruction  
    - SlopeInstability, Debris, BankErosion, Drought, Flood  
  - Impact → FishPassageBarrier, IncreasedSedimentation, ReducedConnectivity, SpawningHabitatScour  
  - Region → OceanBasin, LandRegion, CountryOrState *(with instances like PacificNorthwest, etc.)*  
  - WaterbodyIdentifier *(separate records linked via `hasIdentifier`)*

### Salmon
- Salmon  
  - Life Stages & Reproduction → Juvenile, Jack, Redd  
  - Demography & Condition → VariationInSexRatio, UnusualMortality  
  - Habitat Pressure → SpawningHabitatDegradation  
  - BiologicalActivity → BiologicalActivity → EnhancedActivity, IntenseActivity  
  - Predators → PredatorObservation → BearPredator, SealPredator  
  - Species → SalmonSpecies → ChinookSalmon, PinkSalmon, CohoSalmon, AtlanticSalmon, ChumSalmon, SockeyeSalmon

### Inspection Details
- InspectionDetails  
  - InspectionMethod *(SOSA/Procedure)* → GroundMethod, AerialMethod  
    - GroundMethod → Bankwalk, StreamWalk, SnorkelSurvey, BoatSurvey, ReddCount, DeadPitch, StripCount, FenceCount  
    - AerialMethod → AerialFixedWing, AerialHelicopter  
  - DetectionMethod, Gear, Protocol, CountType, EffortUnit, MediaObject, Person, Organization, Role, Permit, DataQualityFlag  
- Inspection *(SOSA ObservationCollection)*  
- Platform *(SOSA Platform)*, Sensor *(SOSA Sensor)*

---

## 2) Proposed class → property mapping

> Key ranges shown in **italics**; datatype properties list their XSD type.

### Environmental
- **LoticWaterBody**: `flowsInto` → *Environmental*  
- **StreamCondition**: `possibleImpact` → *Impact*  
- **Environmental (all waterbodies)**: `hasIdentifier` → *WaterbodyIdentifier* ; `officialName` (string), `localName` (string), `skos:altLabel` (string list), `geo:lat` (xsd:decimal), `geo:long` (xsd:decimal) *(optional; add per instance)*  
- **WaterbodyIdentifier**: `identifierCode` (string), `identifierScheme` (string), `issuingAuthority` (string), `identifierSource` (xsd:anyURI), `validFrom` (xsd:date), `validTo` (xsd:date)  
- **Region**: `partOf` → *Region*

### Salmon
- **Salmon (general)**: `indicativeOfImpact` → *Impact*  
- **SalmonSpecies**: `scientificName` (string), `foundInRegion` → *Region* ; `skos:altLabel` (string list)

### Inspection Details / SSN-SOSA
- **Inspection (SOSA ObservationCollection)**:  
  - `hasMethod` → *InspectionMethod* (subPropertyOf `sosa:usedProcedure`)  
  - `observedAtWaterBody` → *Environmental* (subPropertyOf `sosa:hasFeatureOfInterest`)  
  - `observedSalmonAspect` → *Salmon* (subPropertyOf `sosa:hasFeatureOfInterest`)  
  - `observedCondition` → *StreamCondition* (subPropertyOf `sosa:hasFeatureOfInterest`)  
  - `inspectionTime` (xsd:dateTime), `fishCount` (xsd:integer), `notes` (string)
- **InspectionMethod (and subtypes)**:  
  - From survey table:  
    - `methodSpeedMinKmH`/`methodSpeedMaxKmH` (xsd:decimal)  
    - `methodSpeedMinKnots`/`methodSpeedMaxKnots` (xsd:decimal)  
    - `dailyCoverageMaxKm` (xsd:decimal), `dailyCoverageNote` (string)  
    - `observerEfficiencyMinPercent`/`observerEfficiencyMaxPercent` (xsd:decimal), `observerEfficiencyNote` (string)  
    - `idealConditions` (string), `limitations` (string)
- **Platform / Sensor**: link methods to platforms with `sosa:isHostedBy`; model observers as *Sensors* hosted by a *Platform*.  
- **Effort & Protocol (optional)**:  
  - `effortValue` (xsd:decimal) + `effortUnit` → *EffortUnit*  
  - `followedProtocol` → *Protocol*  
  - `usedDetection` → *DetectionMethod*  
  - `usedGear` → *Gear*  
  - `observer` → *Person* (subPropertyOf `prov:wasAssociatedWith`) ; `affiliatedWith` → *Organization*

---

### Notes
- Cross-file references (e.g., `:foundInRegion` → `:Region`, `:indicativeOfImpact` → `:Impact`) are intentional; load all three TTLs together.
- `:description` is defined in each file for convenience; identical definitions merge cleanly under RDF semantics.
