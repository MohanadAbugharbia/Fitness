#!/bin/bash


WORKDIR=$PWD

STAGE=${STAGE:-"prod"}

SOURCE_BUCKET=$(aws cloudformation describe-stack-resources --stack-name Fitness-App-Source-Bucket-${STAGE} | jq ".StackResources[].PhysicalResourceId" | sed -r 's/"//g' |grep source)
ROOT_BUCKET=$(aws cloudformation describe-stack-resources --stack-name Fitness-App-Source-Bucket-${STAGE} | jq ".StackResources[].PhysicalResourceId" | sed -r 's/"//g' |grep root)

mkdir -p lambda/dependencies/python
cd lambda/dependencies
python3.10 -m pip install -r $WORKDIR/requirements.txt -t ./python
zip -qr python_dependencies.zip ./python
aws s3 cp --quiet python_dependencies.zip s3://$SOURCE_BUCKET/dependencies/python_dependencies.zip
rm -r python_dependencies.zip python/
cd $WORKDIR

cd lambda/python_app
zip -qr python_app.zip .
aws s3 cp --quiet python_app.zip s3://$SOURCE_BUCKET/functions/python_app.zip
rm python_app.zip
cd $WORKDIR

cd static
aws s3 sync ./ s3://$ROOT_BUCKET/static
cd $WORKDIR
