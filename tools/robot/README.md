# ROBOT CLI Wrapper

This repository bundles ROBOT in `tools/robot/robot.jar` with a wrapper script
`tools/robot/robot`. Add the directory to your `PATH` to use the command:

```bash
export PATH="$(pwd)/tools/robot:$PATH"
```

Optionally add that line to a shell profile to make it persistent. Adjust
`ROBOT_JAVA_ARGS` to control JVM memory, for example:

```bash
export ROBOT_JAVA_ARGS="-Xms1G -Xmx6G"
```

The wrapper targets the Homebrew OpenJDK 17 install at
`/usr/local/opt/openjdk@17/bin/java`. Update the `tools/robot/robot` script if
you move Java elsewhere.
