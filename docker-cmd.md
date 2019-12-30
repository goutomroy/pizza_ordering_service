docker -v  
 docker-compose -v  
 docker version  
 docker-compose down -v  
 docker-compose build  
 docker-compose run web python manage.py migrate  
 docker-compose exec web python manage.py createsuperuser  
 docker ps --size
 docker-compose up  
 docker-compose up --remove-orphans  
 docker exec -it 622756b310bc /bin/sh  