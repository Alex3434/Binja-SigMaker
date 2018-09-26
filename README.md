# SigMaker (v1.1 alpha)
Author: **Alex3434**

SigMaker plugin for Binary Ninja

## Description:

Generate Signatures to use for pattern scanning in other applications.

- The signature has the same form like the sequence of bytes in IDA (eg. 89 45 FC FF 15 ? ? ? ?)
- You can create a signature at any point inside a function.  
- If there is no unique signature at that possition, the plugin will create a signature for the beginning of the function.

## Usage:

<img src="https://i.gyazo.com/bdd6d7a421d14efc6e6128dc5b797fb4.gif"/>
<img src="https://i.gyazo.com/24b4ac1e07dcb08e156535744763afb6.gif"/>


## Minimum Version

This plugin requires the following minimum version of Binary Ninja:

 * release - 9999
 * dev - 1.0.dev-576


## Required Dependencies

The following dependencies are required for this plugin: None



## License

This plugin is released under a [MIT](LICENSE) license.


