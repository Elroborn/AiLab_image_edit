docker build -t registry-vpc.cn-shanghai.aliyuncs.com/shuzhi/image_edit:$1 -f docker/Dockerfile .
docker push registry-vpc.cn-shanghai.aliyuncs.com/shuzhi/image_edit:$1
