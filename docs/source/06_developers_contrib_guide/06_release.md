# Release Process for QHub

In order to create a release:

1. Make sure the `RELEASE.md` is up to date with change, bug fixes,
   and breaking changes and move all the `Upcoming Release` into a new
   section titled `Release <version> - <month>/<day>/<year>`

2. Update file `qhub/VERSION` to be `<version>`

3. Commit these changes to `main` branch

4. Create a Release branch in [Quansight/qhub-terraform-modules](https://github.com/quansight/qhub-terraform-modules) with name `release-<version>` off of the `main` branch.

5. Create a Release branch in [Quansight/qhub](https://github.com/Quansight/qhub) with name `release-<version>` off of the `main` branch.

6. Finally [create a Release on QHub](https://github.com/Quansight/qhub/releases/new). The tag should be `v<version>` off of branch `release-<version>` (**not main**!). Use the `RELEASE.md` to get the title `Release <version> - <month>/<day>/<year>` and set the text description to the `RELEASE.md` for the given version. Click `Publish Release`.

If this worked a new version will be [uploaded to pypi for QHub](https://pypi.org/project/qhub/)
