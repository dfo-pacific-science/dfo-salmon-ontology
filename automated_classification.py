#!/usr/bin/env python3
"""
Automated Classification Demo for DFO Salmon Ontology
Demonstrates the logic for assigning Hyatt 1997 estimate types
"""

import rdflib
from pathlib import Path

def load_data():
    """Load the ontology and sample data"""
    ontology_file = Path("dfo-salmon.ttl")
    data_file = Path("sample-survey-data.ttl")
    
    graph = rdflib.Graph()
    graph.parse(ontology_file, format="turtle")
    graph.parse(data_file, format="turtle")
    
    return graph

def classify_survey(survey_uri, graph):
    """Classify a survey event based on its metadata"""
    
    # Get survey metadata
    query = """
    PREFIX dfo: <https://w3id.org/dfo/salmon#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?enumMethod ?estMethod ?visits ?coverage ?visibility ?efficiency ?riverSwam ?hasDoc
    WHERE {
        ?survey a dfo:EscapementSurveyEvent ;
            dfo:usesEnumerationMethod ?enumMethod ;
            dfo:usesEstimateMethod ?estMethod ;
            dfo:measuredVisits ?visits ;
            dfo:measuredReachCoverage ?coverage ;
            dfo:measuredVisibility ?visibility .
        OPTIONAL { ?survey dfo:measuredObserverEfficiency ?efficiency }
        OPTIONAL { ?survey dfo:percentRiverSwam ?riverSwam }
        OPTIONAL { ?survey dfo:hasDocumentation ?hasDoc }
    }
    """
    
    results = list(graph.query(query, initBindings={'survey': survey_uri}))
    if not results:
        return None, []
    
    row = results[0]
    enum_method = str(row.enumMethod).split('#')[-1] if '#' in str(row.enumMethod) else str(row.enumMethod)
    est_method = str(row.estMethod).split('#')[-1] if '#' in str(row.estMethod) else str(row.estMethod)
    visits = int(row.visits) if row.visits else 0
    coverage = float(row.coverage) if row.coverage else 0.0
    visibility = str(row.visibility) if row.visibility else "Unknown"
    efficiency = float(row.efficiency) if row.efficiency else None
    river_swam = float(row.riverSwam) if row.riverSwam else None
    has_doc = bool(row.hasDoc) if row.hasDoc else False
    
    # Apply classification logic
    estimate_type = None
    downgrade_criteria = []
    
    # Snorkel Survey Classification
    if enum_method == "VisualSnorkelCount":
        if visits >= 5 and coverage >= 0.8 and visibility in ["Good", "Excellent"]:
            estimate_type = "Type2"
        elif visits >= 3 and coverage >= 0.5:
            estimate_type = "Type3"
        elif visits <= 2:
            estimate_type = "Type4"
        else:
            estimate_type = "Type5"
        
        # Check downgrade criteria
        if visits <= 4:
            downgrade_criteria.append("VISITS")
        if coverage < 0.8:
            downgrade_criteria.append("REACH_COVERAGE")
        if visibility in ["Poor", "Fair"]:
            downgrade_criteria.append("VISIBILITY")
        if not has_doc:
            downgrade_criteria.append("DOC")
    
    # Aerial Survey Classification
    elif enum_method == "AerialSurveyCount":
        if visits >= 3 and coverage >= 0.8 and visibility in ["Good", "Excellent"]:
            estimate_type = "Type3"
        elif visits <= 2:
            estimate_type = "Type4"
        else:
            estimate_type = "Type5"
        
        # Check downgrade criteria
        if visits <= 2:
            downgrade_criteria.append("VISITS")
        if coverage < 0.8:
            downgrade_criteria.append("REACH_COVERAGE")
        if visibility in ["Poor", "Fair"]:
            downgrade_criteria.append("VISIBILITY")
        if not has_doc:
            downgrade_criteria.append("DOC")
    
    # Other methods
    else:
        estimate_type = "Type5"
        downgrade_criteria.append("UNKNOWN_METHOD")
    
    return estimate_type, downgrade_criteria

def main():
    """Main function to demonstrate automated classification"""
    
    print("=== DFO Salmon Ontology Automated Classification Demo ===\n")
    
    # Load data
    graph = load_data()
    
    # Get all survey events
    query = """
    PREFIX dfo: <https://w3id.org/dfo/salmon#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?survey ?label
    WHERE {
        ?survey a dfo:EscapementSurveyEvent ;
            rdfs:label ?label .
    }
    ORDER BY ?survey
    """
    
    results = graph.query(query)
    
    print("Survey Classification Results:")
    print("=" * 80)
    print(f"{'Survey':<30} {'Type':<8} {'Downgrade Criteria':<30}")
    print("=" * 80)
    
    for row in results:
        survey_uri = row.survey
        label = str(row.label) if row.label else "Unknown"
        
        estimate_type, downgrade_criteria = classify_survey(survey_uri, graph)
        
        if estimate_type:
            downgrade_str = ", ".join(downgrade_criteria) if downgrade_criteria else "None"
            print(f"{label:<30} {estimate_type:<8} {downgrade_str:<30}")
        else:
            print(f"{label:<30} {'ERROR':<8} {'Could not classify':<30}")
    
    print("\n" + "=" * 80)
    print("Classification Logic Summary:")
    print("- Type 2: Snorkel with ≥5 visits, ≥80% coverage, good/excellent visibility")
    print("- Type 3: Snorkel with ≥3 visits, ≥50% coverage OR Aerial with ≥3 visits, ≥80% coverage, good/excellent visibility")
    print("- Type 4: Snorkel with ≤2 visits OR Aerial with ≤2 visits")
    print("- Type 5: Other conditions")
    print("\nDowngrade Criteria:")
    print("- VISITS: Too few visits for high precision")
    print("- REACH_COVERAGE: Insufficient spatial coverage")
    print("- VISIBILITY: Poor visibility conditions")
    print("- DOC: Missing documentation")

if __name__ == "__main__":
    main()
