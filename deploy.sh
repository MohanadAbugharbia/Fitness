#!/bin/bash

WORKDIR=$PWD
set -x


[[ -n $STAGE ]] || {
    echo "Env var STAGE has to be set." 1>&2
    exit -1
}
[[ -n $COGNITO_DOMAIN_NAME ]] || {
    echo "Env var COGNITO_DOMAIN_NAME has to be set." 1>&2
    exit -1
}
[[ -n $APP_DOMAIN_NAME ]] || {
    echo "Env var APP_DOMAIN_NAME has to be set." 1>&2
    exit -1
}
[[ -n $CDN_DOMAIN_NAME ]] || {
    echo "Env var CDN_DOMAIN_NAME has to be set." 1>&2
    exit -1
}
[[ -n $FLASK_SECRET_KEY ]] || {
    echo "Env var FLASK_SECRET_KEY has to be set." 1>&2
    exit -1
}
[[ -n $DOMAIN ]] || {
    echo "Env var DOMAIN has to be set." 1>&2
    exit -1
}
[[ -n $HOSTED_ZONE_ID ]] || {
    echo "Env var HOSTED_ZONE_ID has to be set." 1>&2
    exit -1
}

if [[ $STAGE != "prod" ]]; then
    DOMAIN="-${STAGE}.${DOMAIN}"
else
    DOMAIN=".${DOMAIN}"
fi

COGNITO_DOMAIN_NAME="${COGNITO_DOMAIN_NAME}${DOMAIN}"
APP_DOMAIN_NAME="${APP_DOMAIN_NAME}${DOMAIN}"
CDN_DOMAIN_NAME="${CDN_DOMAIN_NAME}${DOMAIN}"

PARAMETERS="Environment=$STAGE CognitoDomainName=$COGNITO_DOMAIN_NAME AppDomainName=$APP_DOMAIN_NAME CDNDomainName=$CDN_DOMAIN_NAME FlaskSecretKey=$FLASK_SECRET_KEY HostedZoneId=$HOSTED_ZONE_ID"
TAGS="Environment=$STAGE"

{
    STACK_NAME="Fitness-App-Source-Bucket-${STAGE}"
    TEMPLATE_FILE="${WORKDIR}/infra/src_bucket.yml"
    CAPABILITIES="CAPABILITY_IAM CAPABILITY_NAMED_IAM"

    aws cloudformation deploy --stack-name $STACK_NAME --template-file $TEMPLATE_FILE --capabilities $(echo $CAPABILITIES) --parameter-override $(echo $PARAMETERS) --tags $(echo $TAGS)
    $WORKDIR/push_sources.sh
} && {
    STACK_NAME="Fitness-App-us-east-1-certificates-${STAGE}"
    TEMPLATE_FILE="${WORKDIR}/infra/us-east-1-certificates.yml"

    aws --region us-east-1 cloudformation deploy --stack-name $STACK_NAME --template-file $TEMPLATE_FILE --parameter-override $(echo $PARAMETERS) --tags $(echo $TAGS)
    COGNITO_CERTIFICATE_ARN=$(aws --region us-east-1 cloudformation describe-stack-resource --stack-name $STACK_NAME --logical-resource-id CognitoCertificate | jq ".StackResourceDetail.PhysicalResourceId" | sed -r 's/"//g')
    CDN_CERTIFICATE_ARN=$(aws --region us-east-1 cloudformation describe-stack-resource --stack-name $STACK_NAME --logical-resource-id CDNCertificate | jq ".StackResourceDetail.PhysicalResourceId" | sed -r 's/"//g')
}&& {
    STACK_NAME="Fitness-App-${STAGE}"
    TEMPLATE_FILE="${WORKDIR}/infra/main.yml"
    PARAMETERS="$PARAMETERS CDNCertificateArn=$CDN_CERTIFICATE_ARN CognitoCertificateArn=$COGNITO_CERTIFICATE_ARN"
    CAPABILITIES='CAPABILITY_IAM CAPABILITY_NAMED_IAM'

    aws cloudformation deploy --stack-name $STACK_NAME --template-file $TEMPLATE_FILE --parameter-override $(echo $PARAMETERS) --capabilities $(echo $CAPABILITIES) --tags $(echo $TAGS)
}