# Garry's Mod
Garry's Mod is amongst our 1st integration for BSA.\
This is created under Lua & MySQLOO drivers, no other dependencies are required.

!!! abstract
	We are still making major changes to this section, as development is not considered released.

	✅ **Environment Progress**
	[=100% "100%"]{: .candystripe .candystripe-animate}

	✅ **Technical Progress**
	[=100% "100%"]{: .candystripe .candystripe-animate}

	🛠️ **Integration Progress** - 🛑 Blocker for public release BSA OSS
	[=70% "70%"]{: .candystripe .candystripe-animate}

	🛠️ **Documentation Progress** - 📝 Under Review
	[=90% "90%"]{: .candystripe .candystripe-animate}

This section is to document the behaviors of toolsets deemed accessible to developers without disrupting core.

<p align="center">
  <img src="preview.png" alt="BSA Logo">
</p>

## Features
- Interface system designed for sleek but powerful management.
- Extremely abstract command system for multi-platform communication.
- Highly configurable and dynamic configuration systems with export/import capabilities.
- Extensive and endless language and theme customizations.
- Plugin systems for direct and togglable attachments to BSA core.
- Multi-server communication and database dispatching.
- Support for BSA's multi-verse of different platforms, services and providers.
- Designed for large communities with diverse player-bases.

## Importing
We cannot compensate for all admin systems and create customized export/import tools for them.\
With this understanding we expect that an individual with DB experience and Lua experience is present.

For ease of importation we allow a mode called "standalone".\
This allows BSA to run with an existing administration system, preventing overrides from occuring.

## Plugins
This platform connector supports an underlying plugin system.\
This is designed to allow you to dynamically enable/disable extended features of the system.

Start with the [plugins overview](modules/plugins.md), then continue to [creating a plugin](modules/plugins/creating.md) for the authoring guide.

## Hooks

- `#!ts BSA.initialize()`\
Fired after all core modules have been loaded and initialized (not connected!).