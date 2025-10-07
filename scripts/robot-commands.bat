@echo off
REM ROBOT Commands for DFO Salmon Ontology
REM Make sure you're in the project directory

echo ROBOT Commands for DFO Salmon Ontology
echo =====================================
echo.

echo Available commands:
echo 1. Validate ontology (reasoning check)
echo 2. Convert to OWL format
echo 3. Convert to JSON format
echo 4. Show ontology metrics
echo 5. Run all checks
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Running reasoning check...
    java -jar tools/robot.jar reason --input ontology/dfo-salmon.ttl --reasoner ELK
    echo Reasoning check completed.
) else if "%choice%"=="2" (
    echo Converting to OWL format...
    java -jar tools/robot.jar convert --input ontology/dfo-salmon.ttl --output release/artifacts/dfo-salmon.owl
    echo Conversion completed. Output: release/artifacts/dfo-salmon.owl
) else if "%choice%"=="3" (
    echo Converting to JSON format...
    java -jar tools/robot.jar convert --input ontology/dfo-salmon.ttl --format json --output release/artifacts/dfo-salmon.json
    echo Conversion completed. Output: release/artifacts/dfo-salmon.json
) else if "%choice%"=="4" (
    echo Computing ontology metrics...
    java -jar tools/robot.jar measure --input ontology/dfo-salmon.ttl --output metrics.txt
    type metrics.txt
    del metrics.txt
) else if "%choice%"=="5" (
    echo Running all checks...
    echo.
    echo 1. Reasoning check...
    java -jar tools/robot.jar reason --input ontology/dfo-salmon.ttl --reasoner ELK
    echo.
    echo 2. Computing metrics...
    java -jar tools/robot.jar measure --input ontology/dfo-salmon.ttl --output metrics.txt
    type metrics.txt
    del metrics.txt
    echo.
    echo 3. Converting to OWL...
    java -jar tools/robot.jar convert --input ontology/dfo-salmon.ttl --output release/artifacts/dfo-salmon.owl
    echo.
    echo 4. Converting to JSON...
    java -jar tools/robot.jar convert --input ontology/dfo-salmon.ttl --format json --output release/artifacts/dfo-salmon.json
    echo.
    echo All checks completed!
) else (
    echo Invalid choice. Please run the script again.
)

echo.
pause
