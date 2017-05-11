Here the link on Db schema http://ondras.zarovi.cz/sql/demo/
Keyword for load - 'Tournament_Football'
Table Tournament_Tour has a connection many to many. Other tables has a connection
one to many or one to one.

I've already told that i did't put folder env and db file into gitignore file.
Maybe it is not so bad. Because you can quickly clone all project and
run it with some data.

All site logic situated in view.py and models.py files.

In view.py file implemented CRUD operations mostly with table Tournament and Team.

In models.py file located models and managers. In future I am going to separate
this file. And here implemented all business logic. The main and the
hardest modules is class TeamManager where calculates teams points in tournament
and MatchManager where generates tournaments schedule. 