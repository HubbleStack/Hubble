docker exec -it `docker ps | grep "hubbledev-centos7-4_gs" | awk '{print $1}'` bash