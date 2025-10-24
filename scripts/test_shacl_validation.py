#!/usr/bin/env python3
"""
Test script for DFO Salmon Ontology SHACL validation
Requires: pip install pyshacl rdflib
"""

import sys
from pathlib import Path
import rdflib
from pyshacl import validate

def test_shacl_validation():
    """Test SHACL validation on sample data"""
    
    # Load the ontology and shapes
    ontology_file = Path("dfo-salmon.ttl")
    shapes_file = Path("dfo-salmon-shapes.ttl")
    data_file = Path("sample-survey-data.ttl")
    
    if not all(f.exists() for f in [ontology_file, shapes_file, data_file]):
        print("Error: Required files not found")
        print(f"Ontology: {ontology_file.exists()}")
        print(f"Shapes: {shapes_file.exists()}")
        print(f"Data: {data_file.exists()}")
        return False
    
    try:
        # Load the data graph
        data_graph = rdflib.Graph()
        data_graph.parse(ontology_file, format="turtle")
        data_graph.parse(data_file, format="turtle")
        
        # Load the shapes graph
        shapes_graph = rdflib.Graph()
        shapes_graph.parse(shapes_file, format="turtle")
        
        print("=== DFO Salmon Ontology SHACL Validation Test ===\n")
        print(f"Data graph size: {len(data_graph)} triples")
        print(f"Shapes graph size: {len(shapes_graph)} triples")
        
        # Run validation
        conforms, results_graph, results_text = validate(
            data_graph,
            shacl_graph=shapes_graph,
            ont_graph=None,
            inference='rdfs',
            abort_on_first=False,
            allow_infos=False,
            allow_warnings=False,
            meta_shacl=False,
            debug=False,
            advanced=False
        )
        
        # Apply the SHACL rules to get assigned types
        conforms2, results_graph2, results_text2 = validate(
            data_graph,
            shacl_graph=shapes_graph,
            ont_graph=None,
            inference='rdfs',
            abort_on_first=False,
            allow_infos=True,
            allow_warnings=True,
            meta_shacl=False,
            debug=False,
            advanced=True
        )
        
        print(f"\nValidation Result: {'PASS' if conforms else 'FAIL'}")
        print(f"Results: {len(results_graph)} validation results")
        
        if results_text:
            print("\nValidation Details:")
            print("=" * 50)
            print(results_text)
        
        # Test automated classification
        print("\n=== Automated Classification Test ===")
        test_automated_classification(data_graph)
        
        return conforms
        
    except Exception as e:
        print(f"Error during validation: {e}")
        return False

def test_automated_classification(data_graph):
    """Test the automated classification rules"""
    
    # Query for survey events and their assigned types
    query = """
    PREFIX dfo: <https://w3id.org/dfo/salmon#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?survey ?label ?enumMethod ?estMethod ?visits ?coverage ?visibility ?assignedType
    WHERE {
        ?survey a dfo:EscapementSurveyEvent ;
            rdfs:label ?label ;
            dfo:usesEnumerationMethod ?enumMethod ;
            dfo:usesEstimateMethod ?estMethod ;
            dfo:measuredVisits ?visits ;
            dfo:measuredReachCoverage ?coverage ;
            dfo:measuredVisibility ?visibility .
    }
    ORDER BY ?survey
    """
    
    results = data_graph.query(query)
    
    print("Survey Events and Classification:")
    print("-" * 80)
    print(f"{'Survey':<25} {'Visits':<6} {'Coverage':<8} {'Visibility':<10} {'Type':<10}")
    print("-" * 80)
    
    for row in results:
        survey = str(row.survey).split('#')[-1] if '#' in str(row.survey) else str(row.survey)
        label = str(row.label) if row.label else "Unknown"
        visits = str(row.visits) if row.visits else "N/A"
        coverage = f"{float(row.coverage):.2f}" if row.coverage else "N/A"
        visibility = str(row.visibility) if row.visibility else "N/A"
        assigned_type = str(row.assignedType).split('#')[-1] if row.assignedType else "Not assigned"
        
        print(f"{label:<25} {visits:<6} {coverage:<8} {visibility:<10} {assigned_type:<10}")
    
    # Query for downgrade criteria
    print("\nDowngrade Criteria Applied:")
    print("-" * 50)
    
    downgrade_query = """
    PREFIX dfo: <https://w3id.org/dfo/salmon#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?survey ?label ?criteria
    WHERE {
        ?survey a dfo:EscapementSurveyEvent ;
            rdfs:label ?label ;
            dfo:downgradeCriteriaMet ?criteria .
    }
    ORDER BY ?survey ?criteria
    """
    
    downgrade_results = data_graph.query(downgrade_query)
    
    if downgrade_results:
        for row in downgrade_results:
            survey = str(row.survey).split('#')[-1] if '#' in str(row.survey) else str(row.survey)
            label = str(row.label) if row.label else "Unknown"
            criteria = str(row.criteria).split('#')[-1] if '#' in str(row.criteria) else str(row.criteria)
            print(f"{label}: {criteria}")
    else:
        print("No downgrade criteria applied (this is expected for valid surveys)")

if __name__ == "__main__":
    success = test_shacl_validation()
    sys.exit(0 if success else 1)
