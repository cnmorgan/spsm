Contributing
============

Branching Model
---------------

spsm uses a branching model based on `this <https://nvie.com/posts/a-successful-git-branching-model/>`_ blog post.
If you would like to make a contribution please create a branch appropriate to the changes you would like to make. For signifigant changes,
or changes you'd like input on before starting, feel free to post an `issue <https://github.com/cnmorgan/spsm/issues/new/choose>`_ first.

The repository is broken up into 5 main branch types:

1. Master -

  This is the main branch that is packaged and released

2. Hotfixes -

  These branches are created off of "master" and are bugfixes that require immediate attention.

3. Dev -

  This branch is where the most new code changes will be merged prior release into "master"

4. Features -

  These branches are created off of "dev" and are used for developing new features that won't be merged into "master" until a new release.

5. Releases -

  These branches are created off of "dev" and are used to prepare for a new release merge into "master"

Master
^^^^^^
This is the primary branch for the project. Changes should never be directly pushed to this branch.

Hotfixes
^^^^^^^^
A hotfix branch should be branched off of "master" and be of the format: :code:`htfx/my-bugfix-name`. Create a hotfix branch for issues in "master" that require immediate
attention that cannot wait until the next release branch is merged.

Dev
^^^
This is the main branch that is used for the development of new features. Most new changes should be branches off of "dev" rather than master except for in
the case of hotfixes.

Features
^^^^^^^^
A feature branch should be branched off of "dev" and be of the format: :code:`ft/my-feature-name`. Feature branches is where the bulk of new development should take place and should be
made for any new feature that is developed for an upcoming release.

Releases
^^^^^^^^
Release branches are branched off from "dev" and formatted as :code:`rel/vX.Y.Z`. These branches will not have any code changes made except for bugfixes and will ultimately
be merged with "master" for a new release.

Versioning
----------

spsm uses semantic version numbers of the following format:

:code:`<major>.<minor>.<patch>`

where:
  - Major is bumped to indicate incompatibility ( i.e. commands that worked in 1.0.1 may not necessarily work in 2.0.0 )
  - Minor is bumped to indicate new feature
  - Patch is bumped to indicate bugfixes

For more info on Semantic Version Numbers see: https://semver.org/

When should I change the Version?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In general, the version number should only be changed for hotfixes and for releases. When a hotfix is created and merged, the patch number can be bumped.
For new release branches, the Major or Minor can be bumped depending on the contents of the new release.