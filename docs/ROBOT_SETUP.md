# ROBOT Setup for DFO Salmon Ontology

ROBOT (ROBOT is an OWL Tool) is now set up and ready to use with your DFO Salmon Ontology.

## What's Installed

- **ROBOT version 1.8.3** (compatible with Java 8)
- **Location**: `tools/robot.jar`
- **Batch script**: `tools/robot.bat` (for easy command-line access)
- **Interactive script**: `robot-commands.bat` (menu-driven interface)

## Quick Start

### Option 1: Interactive Menu
Run the interactive script for easy access to common commands:
```cmd
robot-commands.bat
```

### Option 2: Direct Commands
Use ROBOT directly with Java:
```cmd
java -jar tools/robot.jar [command] [options]
```

## Common Commands

### Validate Ontology (Reasoning Check)
```cmd
java -jar tools/robot.jar reason --input ontology/dfo-salmon.ttl --reasoner ELK
```

### Convert to Different Formats
```cmd
# Convert to OWL format
java -jar tools/robot.jar convert --input ontology/dfo-salmon.ttl --output release/artifacts/dfo-salmon.owl

# Convert to JSON format
java -jar tools/robot.jar convert --input ontology/dfo-salmon.ttl --format json --output release/artifacts/dfo-salmon.json
```

### Get Ontology Metrics
```cmd
java -jar tools/robot.jar measure --input ontology/dfo-salmon.ttl --output metrics.txt
```

### Get Help
```cmd
java -jar tools/robot.jar --help
java -jar tools/robot.jar [command] --help
```

## Current Ontology Stats

Based on the latest metrics:
- **Classes**: 123
- **Object Properties**: 30
- **Data Properties**: 25
- **Individuals**: 36
- **Total Axioms**: 1,025
- **OWL Profile**: OWL 2 (not DL/EL/QL/RL)

## Notes

- ROBOT 1.8.3 is used for compatibility with Java 8
- The ontology passes reasoning checks (no logical inconsistencies)
- All commands have been tested and work correctly
- The interactive script provides a user-friendly way to run common operations

## Troubleshooting

If you encounter issues:
1. Make sure Java 8+ is installed: `java -version`
2. Check that you're in the project directory
3. Use `-vvv` flag for detailed error messages: `java -jar tools/robot.jar -vvv [command]`
