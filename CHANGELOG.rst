Changelog
=========

Versioning is based on Django: ``<django major>.<django minor>.<starter release>``


4.2.2 - 2024-12-19
------------------

Change

* Docker store moved from ``store`` to ``docker-store`` to simplify sync filtering. To
  upgrade, shut down containers, update ``compose.yml``, rename store dir, restart.



4.2.1 - 2024-10-30
------------------

Fix:

* Add missing files, replace compose with correct version


4.2.0 - 2024-10-28
------------------

Initial public release
