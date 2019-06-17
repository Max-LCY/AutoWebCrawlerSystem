STACK_NAME=testing
echo "Deploy $STACK_NAME stack"
export AWS_DEFAULT_REGION=us-east-1
AWSAccountId=$(aws sts get-caller-identity --query 'Account' --output text)
SourceBucket=sourcebucketname$AWSAccountId

aws s3 mb s3://$SourceBucket
aws s3 sync infrastructure s3://$SourceBucket/infrastructure 

mkdir ScheduledEcs/build
cp ScheduledEcs/raw/* ScheduledEcs/build/
pip install -r ScheduledEcs/requirements.txt -t ScheduledEcs/build
cp master.yaml ScheduledEcs/build/
cd ScheduledEcs/build/

aws cloudformation package \
    --template-file master.yaml \
    --s3-bucket $SourceBucket \
    --output-template-file packaged.yaml

aws cloudformation deploy \
   --template-file packaged.yaml \
   --stack-name $STACK_NAME \
   --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
   --parameter-overrides \
        S3URL=$SourceBucket
        
$(aws ecr get-login --no-include-email --region us-east-1)
cd ~/environment/Spider/services/hkdoctors
docker build -t $STACK_NAME .
docker tag $STACK_NAME:latest $AWSAccountId.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$STACK_NAME:latest
docker push $AWSAccountId.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$STACK_NAME:latest