## BetterLogServer

This program provides a highly configurable UDP and TCP log collection server using the BSD format.

The program is divided into the following parts:
- Logserver.py - The main file
- Config.py - The log server global configuration
- lib - Contains parsers and other utilities for the main server
- Statistics - Contains statistics gatherers imported in config 
- Identifiers - Contains filters imported in config 
- Engines - Contains methods for saving or forwarding logs, imported in config 
- Tools - Contains tools such as a live view or import tool.
