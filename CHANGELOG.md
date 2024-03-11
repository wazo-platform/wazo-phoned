Changelog
=========

24.05
-----

* Added the DND and forwards status synchronization for Fanvil phones
* Added the following endpoints:

  * GET `/0.1/fanvil/users/<uuid>/services/dnd/enable`
  * GET `/0.1/fanvil/users/<uuid>/services/dnd/disable`

20.11
-----

* Added the following token-authenticated endpoints:

  * PUT `/0.1/endpoints/<endpoint_name>/hold/start`
  * PUT `/0.1/endpoints/<endpoint_name>/hold/stop`

20.06
-----

* Added the DND and forwards status synchronization for Yealink phones
* Added the following endpoints:

  * GET `/0.1/yealink/users/<uuid>/services/dnd/enable`
  * GET `/0.1/yealink/users/<uuid>/services/dnd/disable`
  * GET `/0.1/yealink/directories/lookup/<profile>`

20.03
-----

* Added a plugin to handle BLF events.

19.17
-----

* Migrated the following endpoints from ``wazo-dird``:

  * GET `/0.1/directories/input/<profile>/aastra`
  * GET `/0.1/directories/lookup/<profile>/aastra`
  * GET `/0.1/directories/lookup/<profile>/yealink`
  * GET `/0.1/directories/input/<profile>/snom`
  * GET `/0.1/directories/lookup/<profile>/snom`
  * GET `/0.1/directories/input/<profile>/polycom`
  * GET `/0.1/directories/lookup/<profile>/polycom`
  * GET `/0.1/directories/lookup/<profile>/gigaset/<user_uuid>`
  * GET `/0.1/directories/lookup/<profile>/htek`
  * GET `/0.1/directories/input/<profile>/cisco`
  * GET `/0.1/directories/lookup/<profile>/cisco`
  * GET `/0.1/directories/menu/<profile>/cisco`
  * GET `/0.1/directories/lookup/<profile>/thomson`
