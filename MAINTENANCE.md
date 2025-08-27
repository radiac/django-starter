# Maintenance

These are notes for maintaining this repository, and will not be needed for normal usage
of this repository.


## Release procedure

1. Update `CHANGELOG.rst` with a new version
2. Build to catch new version number
   ```bash
   python build.py --delete
   ```
3. Commit and push


## Upgrade Django

To upgrade the base Django in this project:

1. Check out the tag pointing at the last base install, `base-django-A.a`
2. Bump pinned versions in `src/requirements.in`
3. Install the latest Django, empty the ``src`` dir, and create a new project with
   `django-admin.py startproject starter`, then ``mv starter src``
4. In the new `settings.py`, after `BASE_DIR` add `class Common(Configuration):`
   and indent the rest of the file
5. Commit on a new branch, `django-B.b`
6. Tag as the new `base-django-B.b`
7. Replay all customisations we made to the last django onto the new django branch with
   ```bash
   git log --oneline django-A.a
   git cherry-pick <first_customisation>^..<last_customisation>
   ```
8. Push new branch and change to use as default branch