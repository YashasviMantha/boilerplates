: '
run this for execution
curl https://raw.githubusercontent.com/YashasviMantha/boilerplates/refs/heads/main/python-init-proj.sh >> init.sh 
chmod +x init.sh
./init.sh
rm ./init.sh
'

touch readme.txt
# mkdir readme.md

curl -o .gitignore https://raw.githubusercontent.com/YashasviMantha/boilerplates/refs/heads/main/python_gitignore
touch Dockerfile
touch .gitlab-ci.yml
touch requirements.txt

mkdir src
mkdir src/utils
curl -o src/utils/logger.py https://raw.githubusercontent.com/YashasviMantha/boilerplates/refs/heads/main/custom_logger.py
touch src/main.py

