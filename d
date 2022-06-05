* [33mcommit aca964afb146aa1ae5fd6a3f332bf39f501036a2[m[33m ([m[1;36mHEAD -> [m[1;32medit[m[33m, [m[1;31morigin/edit[m[33m)[m
[31m|[m Author: unknown <nestigd95@live.com>
[31m|[m Date:   Sat Jun 4 23:17:36 2022 +0200
[31m|[m 
[31m|[m     updated readme, saved changes to views.py
[31m|[m 
* [33mcommit 12df0691dd703cbde031316fccf8d171db26602f[m
[31m|[m Author: unknown <nestigd95@live.com>
[31m|[m Date:   Sat Jun 4 23:13:25 2022 +0200
[31m|[m 
[31m|[m     completed implementation of edit() in views.py. Tested against potential client side tinkering
[31m|[m 
* [33mcommit 53f3098b085e3e0ddebc196db65ec8743bea2e1f[m
[31m|[m Author: unknown <nestigd95@live.com>
[31m|[m Date:   Sat Jun 4 18:57:12 2022 +0200
[31m|[m 
[31m|[m     edit function implementation in front end comleted
[31m|[m     various bug fixes
[31m|[m     added userIsAuthenticated variable to layout template
[31m|[m     TODO: views.py -> access edited text -> get post -> change data -> save()
[31m|[m 
* [33mcommit c65a4811135c1120e51b1120ac0b8d7e3e232480[m
[31m|[m Author: unknown <nestigd95@live.com>
[31m|[m Date:   Sat Jun 4 00:11:01 2022 +0200
[31m|[m 
[31m|[m     STARTED WORKING ON EDITABLE POSTS. Generated new branch and did little else
[31m|[m 
* [33mcommit 3657715ed541b205e2f0698861a5d34dab9152da[m[33m ([m[1;31morigin/main[m[33m, [m[1;32mmain[m[33m)[m
[31m|[m Author: nestigd <44973652+nestigd@users.noreply.github.com>
[31m|[m Date:   Fri Jun 3 23:20:47 2022 +0200
[31m|[m 
[31m|[m     Update README.md
[31m|[m   
*   [33mcommit 7c5410076b068255efdbfab8fd991691ba7fe786[m
[32m|[m[33m\[m  Merge: 24cb536 71c8da1
[32m|[m [33m|[m Author: nestigd <44973652+nestigd@users.noreply.github.com>
[32m|[m [33m|[m Date:   Fri Jun 3 23:18:39 2022 +0200
[32m|[m [33m|[m 
[32m|[m [33m|[m     Merge pull request #3 from nestigd/pagination
[32m|[m [33m|[m     
[32m|[m [33m|[m     Pagination
[32m|[m [33m|[m 
[32m|[m * [33mcommit 71c8da1daace694e28b2f40399dfae2e15700dd0[m[33m ([m[1;31morigin/pagination[m[33m, [m[1;32mpagination[m[33m)[m
[32m|[m [33m|[m Author: unknown <nestigd95@live.com>
[32m|[m [33m|[m Date:   Fri Jun 3 23:14:14 2022 +0200
[32m|[m [33m|[m 
[32m|[m [33m|[m      improved updatePaginator() in index.js. now USER pages can be changed properly
[32m|[m [33m|[m     it was not necessary to rework the url structure. The problem was solved with the addition of 2 condition checks
[32m|[m [33m|[m 
[32m|[m * [33mcommit 1b1e7439834ed420f3bd65c78c93ce4b37affc17[m
[32m|[m [33m|[m Author: Nestor Gonzalez Dacosta <nestigd95@live.com>
[32m|[m [33m|[m Date:   Fri Jun 3 18:12:45 2022 +0200
[32m|[m [33m|[m 
[32m|[m [33m|[m     finished implementing pagination. 1 bug found
[32m|[m [33m|[m     USER has to become a filter parameter like ALL and FOLLOW are already. It is the proper way
[32m|[m [33m|[m 
[32m|[m * [33mcommit 3bcec6360939305c02715c40aa3026103d690262[m
[32m|[m [33m|[m Author: Nestor Gonzalez Dacosta <nestigd95@live.com>
[32m|[m [33m|[m Date:   Fri Jun 3 17:42:44 2022 +0200
[32m|[m [33m|[m 
[32m|[m [33m|[m     fixed bug in views.py index
[32m|[m [33m|[m 
[32m|[m * [33mcommit 88ead26e5dcba4682f97414cb075924b4dbf6e09[m
[32m|[m [33m|[m Author: Nestor Gonzalez Dacosta <PgCom130@profilglass.local>
[32m|[m [33m|[m Date:   Fri Jun 3 17:34:48 2022 +0200
[32m|[m [33m|[m 
[32m|[m [33m|[m     index view: removed useless call to database
[32m|[m [33m|[m 
[32m|[m * [33mcommit b35d129dd03123bef33b6bff5eaf19697b6943b1[m
[32m|[m [33m|[m Author: Nestor Gonzalez Dacosta <PgCom130@profilglass.local>
[32m|[m [33m|[m Date:   Fri Jun 3 15:05:21 2022 +0200
[32m|[m [33m|[m 
[32m|[m [33m|[m     modified views.py - implemented pagination in back end
[32m|[m [33m|[m     now implementing on front end
[32m|[m [33m|[m     created updatePaginator() in inedx.js
[32m|[m [33m|[m 
[32m|[m * [33mcommit df2576d4417717827304654d26cb4e5455855616[m
[32m|[m [33m|[m Author: Nestor Gonzalez Dacosta <PgCom130@profilglass.local>
[32m|[m [33m|[m Date:   Fri Jun 3 11:05:39 2022 +0200
[32m|[m [33m|[m 
[32m|[m [33m|[m     changes to url behaviour to adapt to pagination
[32m|[m [33m|[m 
[32m|[m * [33mcommit e158edc16c181e59cff9ce88c6fc51d7e9ff3525[m
[32m|[m [33m|[m Author: unknown <nestigd95@live.com>
[32m|[m [33m|[m Date:   Fri Jun 3 00:05:16 2022 +0200
[32m|[m [33m|[m 
[32m|[m [33m|[m     small improvements
[32m|[m [33m|[m 
[32m|[m * [33mcommit d9e85027c31383cfc45ef13e5379eee07e505def[m
[32m|[m[32m/[m  Author: unknown <nestigd95@live.com>
[32m|[m   Date:   Thu Jun 2 23:41:55 2022 +0200
[32m|[m   
[32m|[m       added dead buttons to html
[32m|[m 
* [33mcommit 24cb53618fb1230b31de1016b9625f121511666f[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Thu Jun 2 22:53:20 2022 +0200
[33m|[m 
[33m|[m     step 4: FOLLOWING completed
[33m|[m     next is step 5: pagination
[33m|[m 
* [33mcommit 5420979c3dde316a4c6ac245d62d665cd62e83eb[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Thu Jun 2 20:27:02 2022 +0200
[33m|[m 
[33m|[m     step 3: PROFILE PAGE - completed
[33m|[m     next step is step 4: FOLLOWING
[33m|[m 
* [33mcommit e0d5d46bde4251d9d7cea7d567669b2999cfe4a4[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Thu Jun 2 20:20:50 2022 +0200
[33m|[m 
[33m|[m     CSS fiddle + minor fixes
[33m|[m 
* [33mcommit 64600e82b40a5871e25eb6c94fd373f0483adb6c[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Thu Jun 2 18:41:21 2022 +0200
[33m|[m 
[33m|[m     added unfollow capability
[33m|[m     changes to changeFollowStatus in index.js - now the Follow button switches automatically to Unfollow and viceversa
[33m|[m     changes to views.py to adapt to the new logic
[33m|[m 
* [33mcommit 89b5034f352c2153451858d8ac63e0e574692eb9[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Thu Jun 2 17:06:38 2022 +0200
[33m|[m 
[33m|[m     merged all .js files
[33m|[m 
* [33mcommit f6a370bccb3b4f1178971d0e8766773658ca48f2[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Tue May 31 23:44:30 2022 +0200
[33m|[m 
[33m|[m     pushed unsaved changes to user.js
[33m|[m 
* [33mcommit e6eab43ff2b719bebda44a19af984a0272b8c321[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Tue May 31 23:43:06 2022 +0200
[33m|[m 
[33m|[m     working on views.py follow() and updated README with TODO list
[33m|[m 
* [33mcommit 22c21028f5d9d5752772bb4bb540443bb9116eae[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Tue May 31 23:07:29 2022 +0200
[33m|[m 
[33m|[m     fixed major bug on Following and Like models
[33m|[m     I should have slept more LOL
[33m|[m 
* [33mcommit 9601c335c7ef792387dc55642096bfa876b0120f[m
[33m|[m Author: nestigd <nestigd95@live.com>
[33m|[m Date:   Sun May 29 17:56:51 2022 +0200
[33m|[m 
[33m|[m     work in progress
[33m|[m     follow API in views.py
[33m|[m     this is the backbone of the API but it needs lots of debugging still
[33m|[m 
* [33mcommit 780d7b54a82a9ed4d2eeb284fbb3f347b67d8e2d[m
[33m|[m Author: nestigd <nestigd95@live.com>
[33m|[m Date:   Sun May 29 16:10:41 2022 +0200
[33m|[m 
[33m|[m     improved posts API.
[33m|[m     the API now can receive an int as filter value. The parameter will be used to find all posts of an user with that id.
[33m|[m 
* [33mcommit 3aafbed61ac41dbd4e93f3c1842ab2f427daa3cc[m
[33m|[m Author: nestigd <nestigd95@live.com>
[33m|[m Date:   Sun May 29 15:58:56 2022 +0200
[33m|[m 
[33m|[m     added user() in views.py
[33m|[m 
* [33mcommit 220fb2a9d34ad30c3a3ac5696bfde7decc378ac4[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Sun May 29 12:09:46 2022 +0200
[33m|[m 
[33m|[m     working on the API following() in views.py
[33m|[m 
* [33mcommit e043b95264bde72cd53d3903044b1b0df699e3f5[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Sun May 29 11:14:38 2022 +0200
[33m|[m 
[33m|[m     added new model
[33m|[m     Like added to models.py. It is now a joining table instead of a prop inside Post
[33m|[m 
* [33mcommit fcd39cff1e0a0b12ccbb9cd7e9618ef46727fbe5[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Sun May 29 10:55:42 2022 +0200
[33m|[m 
[33m|[m     improvements:
[33m|[m     properly routed the All Posts nav button
[33m|[m     added configurable link at the top of the .js file for the posts API
[33m|[m     now hiding the form for new posts when the user is not logged in
[33m|[m 
* [33mcommit b081187200fd8685959132a784046dbfe72d31d4[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Sun May 29 10:00:07 2022 +0200
[33m|[m 
[33m|[m     completed functions makePostDiv() and getPost()
[33m|[m 
* [33mcommit a7789bc448e825139e5776d46827ee81481fbdd4[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Sat May 28 15:13:37 2022 +0200
[33m|[m 
[33m|[m     added new Following model
[33m|[m 
* [33mcommit 4dffb2e5aae48a46bcf5ea09496e7842e7ea0739[m
[33m|[m Author: nestigd <44973652+nestigd@users.noreply.github.com>
[33m|[m Date:   Sat May 28 14:57:48 2022 +0200
[33m|[m 
[33m|[m     Update README.md
[33m|[m 
* [33mcommit 9f9f1d5eb6a7ef46b4fe41ad6632bb6e7859fa4b[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Sat May 28 00:24:38 2022 +0200
[33m|[m 
[33m|[m     fixed bug: wrong function name
[33m|[m 
* [33mcommit bcab053c2c9c4aaf676b20e9dc1509db4ef949ab[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Sat May 28 00:21:43 2022 +0200
[33m|[m 
[33m|[m     worked on index.js:
[33m|[m     deleted useless onclick handler
[33m|[m     added work in progress getPost() and makePostDiv()
[33m|[m     TODO: finish implementation of /posts/all both on back and front-end side
[33m|[m 
* [33mcommit 29273ffd835bc1521ff512535e398791c10a3cd2[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Fri May 27 23:45:23 2022 +0200
[33m|[m 
[33m|[m     deleted old posts function on views.py
[33m|[m     now posts are submitted as POST request to the INDEX view.
[33m|[m     created new posts function in views.py. Now this handles a GET request and will send a JSON file with post information
[33m|[m 
* [33mcommit 2bf06d51f501c3ad6d2cbb99dfdc47f05673a3e8[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Fri May 27 22:13:46 2022 +0200
[33m|[m 
[33m|[m     changes do models.py
[33m|[m     fixed Post model: fixed likes field, added -edited on-
[33m|[m     fixed admin site Post display adding all meaningful info
[33m|[m 
* [33mcommit eb3a00cb9f4b769a43f761f49835658f58cf8dc4[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Wed May 25 23:49:31 2022 +0200
[33m|[m 
[33m|[m     Enhanced: new_post form
[33m|[m     Improved (and fixed): Post class in models.py
[33m|[m     Added: post() view in views.py to handle the post submissions
[33m|[m     Added: admin page and registered models in admin.py
[33m|[m     TODO: improve admin page. Cannot see post timestamps at the moment.
[33m|[m     TODO: API to get posts from the back-end
[33m|[m 
* [33mcommit 69c120a8089a13b914cafd1c5bb7c8e185da1613[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Tue May 24 23:31:21 2022 +0200
[33m|[m 
[33m|[m     fixed bug: JS files were not loaded by the browser.
[33m|[m     freature NEW POST: work in progress. Added event listener to the SHARE button
[33m|[m     TODO: Pass the post information to the backend.
[33m|[m     TODO: Check that timestamp and all the rest is correctly generated upon submission
[33m|[m 
* [33mcommit fa7cb01aa2a154057378560bb4b7a828f496e098[m
[33m|[m Author: unknown <nestigd95@live.com>
[33m|[m Date:   Tue May 24 21:47:35 2022 +0200
[33m|[m 
[33m|[m     fixed: Post class in models.py
[33m|[m   
*   [33mcommit 979f6c16abf354f2da62657cad9d890ed28643ba[m
[34m|[m[35m\[m  Merge: 31dd87e 169d38e
[34m|[m [35m|[m Author: unknown <nestigd95@live.com>
[34m|[m [35m|[m Date:   Tue May 24 00:07:13 2022 +0200
[34m|[m [35m|[m 
[34m|[m [35m|[m     Merge branch 'main' of https://github.com/nestigd/network
[34m|[m [35m|[m 
[34m|[m * [33mcommit 169d38e43846b776b29b1a1eeca91a4100566ddc[m
[34m|[m [35m|[m Author: nestigd <44973652+nestigd@users.noreply.github.com>
[34m|[m [35m|[m Date:   Mon May 23 16:54:04 2022 +0200
[34m|[m [35m|[m 
[34m|[m [35m|[m     Create README.md
[34m|[m [35m|[m 
* [35m|[m [33mcommit 31dd87eeeceed6ee5800bcc7733b9898981cfbce[m
[35m|[m[35m/[m  Author: unknown <nestigd95@live.com>
[35m|[m   Date:   Tue May 24 00:06:42 2022 +0200
[35m|[m   
[35m|[m       Index.html: made form to add new posts. models.py: started creation of a model for posts. Laid basic CSS structure
[35m|[m 
* [33mcommit 57270b9599ab7645475baf2cc9c1f2aa799f94c0[m
  Author: unknown <nestigd95@live.com>
  Date:   Sun May 22 23:50:01 2022 +0200
  
      initial commit. only distribution code
