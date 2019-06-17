npm uninstall -g aws-sam-local
sudo rm $(which sam)
sudo yum -y update
sudo yum -y install aws-cli
pip install --user aws-sam-cli
sudo -H pip install awscli --upgrade
alias sam=~/.local/bin/sam
sam --version
ln -sfn ~/.local/bin/sam ~/.c9/bin/sam

