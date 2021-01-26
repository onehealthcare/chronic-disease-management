for i in {1..4}
do
    echo retart web-template_web_$i...
    docker stop web-template_web_$i && docker exec -it web-template_nginx_1 nginx -s reload
    docker start web-template_web_$i && docker exec -it web-template_nginx_1 nginx -s reload
    echo done

done
