# BSA

:wave: Hello and welcome to Buildstruct Admen.\
A monolithic community system for multi-platform communities.\
As long as any platform supports SQL connectors, this system will work anywhere.

BlueShank - Project Leader, Programmer, Library, Database\
Bonyoze - Project Maintainer, BSU Acquisition, Player Picker Prefixes\
Srlion - Library SFS, Library SFB\
Buildstruct - Development Environments, Developer Assistants

!!! danger
	This site is still under active development & project changes.\
	You may find issues with this site, we recommend you report them when found.

!!!abstract
    We are still making major changes to this section, as development is not considered released.\
    **BASELINE 1.0** is in relation to the release to Buildstruct, not public.

## Database
The actual functionality behind BSA is highly dependant on the database.\
All other projects simply attach to the database to function properly, without it everything breaks.

## Platforms
All of BSA is separated into platform-specific projects, except for the database.\
Each platform must adhere to BSA's database design, any deviations may cause other platform projects to fail.

!!! warning
	We recommend that those looking to install do not use platforms that aren't verified by us.\
	This leaves you open to attacks directly to the database itself!

## Development Cycle
There are some limits to our capabilities to developing BSA to its fullest potential:

- "One-Man Army" Development Flow
- Buildstruct Development Environments

Because of this, issue trackers and pull requests maybe significantly slowed compared to a full team.

### Contributing
We allow everyone within reason to contribute to our work on BSA.\
BSA will REMAIN a free and open-source project.

There are some rules that must be known for contributors:

!!! danger
	Not following these rules may result in Issue/PRs being closed/deleted!

- "spaces" vs "tabs"
    - We generally don't have a preference but mixing the two in a single file is not something we would want.
    - Please make sure you do not commit changes with spacing/tabs changing as well, this will make history difficult to view.
- Keep it Apache-2.0 friendly
    - Share code/docs/assets you have the rights to contribute.
    - Avoid copy-pasting from incompatible licensed sources.
- Keep pull requests clean
    - One topic per pull request (feature, fix, docs, or refactor).
    - Update docs/tests when your change affects behavior.
- Keep the project safe
    - Never commit secrets, tokens, private keys, or private user data.
- Keep style consistent
    - Follow the style in files you touch and avoid large formatting-only rewrites.
- Keep it respectful
    - Be constructive in issues and reviews.
    - Maintainers have final say on merge decisions.

## Project Tracker
We have an actively maintained project tracker for this system.\
For future updates and expectancy on changes we recommend keeping track of this.

[Buildstruct Admen Project Tracker](https://github.com/orgs/Buildstruct/projects/4)
(This may be private)

## Project Domains

### Core
[BSA Database - CORE](https://github.com/Buildstruct/bsa-core-database)

- Database playbook for setting up the SQL tables and necessary data.

### Garry's Mod
[BSA Platform - GMOD](https://github.com/Buildstruct/bsa-platform-gmod)

- Core platform for Garry's Mod

[BSA Platform Plugins - GMOD](https://github.com/Buildstruct/bsa-plugin-gmod)

- Contains a collection of plugins by contributors of BSA.

[BSA Platform Plugins (PRIVATE) - GMOD](https://github.com/Buildstruct/bsa-plugin-gmod-private)

- Since this is specific to buildstruct we are reserving the right to this.

### SourceMod
Do note sourcemod supports a wide variety of games under source engine.\
[BSA Platform - SM](https://github.com/Buildstruct/bsa-plugin-gmod-private)
