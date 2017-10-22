# EpicMonopoly
A novel developed monopoly based on web: EpicMonopoly 

Server structure: 

- [ ] Web server: nginx
- [ ] Database: mongoDB
- [ ] Application server: tornado
- [ ] Cache server: redis

## Details

- Web server is used to listen in the port and deal with queries from front end directly, for:
	+ static page query will be handled in nginx
	+ dynamic page query will be transfer to application server
- Application is used to deal with game logic and the query sent from nginx
- Database stores game data and is used for data IO operation. Main database is mongoDB
- Redis is not the main database but is used as a cache server for accelerating


