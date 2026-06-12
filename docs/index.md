# :wave: Home

**BSA** is a community management system built around a single SQL database that every platform connects to directly.\
Player accounts, groups, permissions, and punishments all live in that shared database, not in per-server configs or a reporting layer on top.

Most multi-platform tools work by wrapping a console or HTTP reporter around your game servers.\
BSA instead integrates at the platform level (Lua in Garry's Mod, SourcePawn in SourceMod), giving each server direct read/write access to the full community state.

This means a group change, a ban, or a player record is immediately available across every connected server and platform.

- **no sync scripts**
- **no external agents**
- **no connection dependencies**

This also means, you get to decide how things work at the platform level, allowing for additional plugins that affect the entire community.

## Overall Progress
We are actively working on supporting as many plaforms as possible & maintaining them.

!!! abstract
	This site is still under active development & project changes.\
	You may find issues with this site, we recommend you report them when found.

	✅ **Database Technical Progress**
	[=100% "100%"]{: .candystripe .candystripe-animate}

	🛠️ **Database Documentation Progress**
	[=90% "90%"]{: .candystripe .candystripe-animate}

	🛠️ **Platform Support Progress**
	[=25% "25%"]{: .candystripe .candystripe-animate}

## Contributors
- BlueShank - Project Leader, Architect, Full-Stack, Database
- Srlion - Garry's Mod Platform Library SFS & SFB
- Bonyoze - Garry's Mod Platform Contributor
- Textstack - Logo Artwork

Thanks to Buildstruct for: Development Environments, Developer Assistants

## Development Cycle
Currently it's a "One-Man Army" Development Flow, meaning development is significantly slowed compared to a full team.\
However we have environments setup and self-hosted solutions to keep-up with possible requests:

- Buildstruct Development Environments
- Self-Hosted Pelican Nodes

---

### AI/LLM Generation
We allow limited AI/LLM usage as an assistive tool, not as a replacement for authorship, understanding, or review.\
If AI/LLM tools were used during a contribution, that usage must be disclosed clearly.\
**Pull Requests, Trackers, and Issues that are primarily AI-generated, spammy, or submitted without human verification will be closed without further notice**.

Contributors are expected to understand, verify, and stand behind what they submit.\
If AI/LLM tools helped with your work, say so and explain the extent of that usage.

#### Allowed

- Explaining concepts and helping understand the codebase.
- Search and navigation of monolithic codebases.
- Drafting documentation and inline function documentation that is reviewed and corrected by a human.
- Research and conceptualization of a feature.
- Small-scale assistance with rewriting, summarizing, or brainstorming.

#### Denied

- Hiding or lying about AI/LLM usage in contributions.
- Creating Pull Requests, Trackers, or Issues directly from AI output without proper human verification or understanding.
- Submitting code, docs, or reports you cannot explain, maintain, or defend.

---

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
