Changelog
=========

20.06
-----

* Added the DND and forwards status synchronization for Yealink phones
* Added the following endpoints:

  * GET `/0.1/yealink/user_service/dnd`
  * GET `/0.1/yealink/user_service/forward_busy`
  * GET `/0.1/yealink/user_service/forward_unconditional`
  * GET `/0.1/yealink/user_service/forward_noanswer`

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
