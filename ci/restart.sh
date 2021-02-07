END=4
for i in $(seq 1 $END)
do
    echo retart web-template_web_$i...
    docker stop web-template_web_$i && docker exec -it web-template_nginx_1 nginx -s reload
    docker start web-template_web_$i && docker exec -it web-template_nginx_1 nginx -s reload
    echo done

done
