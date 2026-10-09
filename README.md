
![Logo](doc/logo.png) intellij-emberjs
===============================================================================

This plugin provides basic [Ember.js](http://emberjs.com/) support to all
[JetBrains](https://www.jetbrains.com/) IDEs that support JavaScript.

fork of https://github.com/Turbo87/intellij-emberjs with additional features


Features
-------------------------------------------------------------------------------

![Navigate → Class...](doc/goto-class.png)
Experimental:
- Handlebars references for tags/mustache paths and tag attributes
- Handlebars autocompletion for tags and mustache paths, also from yields and named yields
- resolves {{or x y z}} to the first resolvable option, this makes {{component (or x y)}} work, e.g in power-select
- Handlebars parameter hints for helpers/modifiers and components
- Handlebars renaming for mustache ids and html tags
- Glint Support
- Gts Support
- Find Usage between Js/Ts and Hbs

Basic:
- Ember.js project discovery when imported from existing sources
- Automatically sets the language level to ES6
- Marks `app`, `public` and `tests` folders as source, resource and test folders
- Marks `node_modules` and `bower_components` as library folders
- Enable JSHint using `.jshintrc`
- Quick navigation via `Navigate → Class...` and `Navigate → Related Symbol...`
  for all major app components
- Generate Ember.js files via `ember generate`
- Basic reference resolving and completion for e.g. `DS.belongsTo('user')`
- Live templates
[more...](doc/features.md)


Installation
-------------------------------------------------------------------------------

This is a fork of [EmberExperimental.js](https://github.com/patricklx/intellij-emberjs-experimental), published as
**EmberExperimental.js (nickschot fork)** under its own plugin ID (`com.emberjs.experimental.nickschot`). It can't be
enabled together with the original plugin, so uninstall that one first.

Releases are published as a custom plugin repository, so the IDE installs and updates the plugin like any other:

1. Settings → Plugins → ⚙ → **Manage Plugin Repositories...** → add

       https://github.com/nickschot/intellij-emberjs-experimental/releases/latest/download/updatePlugins.xml

2. Search the **Marketplace** tab for "EmberExperimental.js (nickschot fork)" and install it.

Each release's zip is also attached to its [GitHub release](https://github.com/nickschot/intellij-emberjs-experimental/releases)
for installing via Settings → Plugins → ⚙ → **Install Plugin from Disk...**.


### From Source

Clone this repository:

    git clone https://github.com/nickschot/intellij-emberjs-experimental.git
    cd intellij-emberjs-experimental

Build a plugin zip file:

    ./gradlew buildPlugin

Install the plugin from `build/distributions/intellij-emberjs-experimental-<version>.zip`:

    Settings → Plugins → ⚙ → Install Plugin from Disk...


Releasing
-------------------------------------------------------------------------------

Run the **Release** workflow from the Actions tab on `main`. It bumps the version in `build.gradle.kts` (patch or
minor, or an exact version you enter), runs the tests and the Plugin Verifier, builds the plugin, commits and tags
`v<version>`, and publishes a GitHub release with the plugin zip and the `updatePlugins.xml` the plugin repository
URL above points at.

The release notes are GitHub's generated notes (the pull requests merged since the previous release). They are
prepended to [CHANGELOG.md](CHANGELOG.md) in the release commit, used as the plugin's change notes (shown in the
IDE's update dialog) and as the GitHub release description.


Development
-------------------------------------------------------------------------------

Run IntelliJ IDEA Ultimate with the current plugin pre-installed:

    ./gradlew runIdea

Run the test suite:

    ./gradlew test


Links
-------------------------------------------------------------------------------

- [JetBrains/intellij-community](https://github.com/JetBrains/intellij-community) – 
  the IntelliJ community edition source code
- [JetBrains/intellij-plugins](https://github.com/JetBrains/intellij-plugins) – 
  a collection of officially supported IntelliJ plugins
- [JetBrains/gradle-intellij-plugin](https://github.com/JetBrains/gradle-intellij-plugin) – 
  the official [Gradle](http://gradle.org/) plugin for building IntelliJ plugins
- [kristianmandrup/emberjs-plugin](https://github.com/kristianmandrup/emberjs-plugin) – 
  the predecessor and inspiration for this plugin


License
-------------------------------------------------------------------------------

This project is licensed under the [Apache 2.0 License](LICENSE).

- [Font-Awesome-SVG-PNG](https://github.com/encharm/Font-Awesome-SVG-PNG) is licensed under the MIT license
- [Font-Awesome](http://fontawesome.io/) is licensed under the [SIL OFL 1.1](http://scripts.sil.org/OFL)
