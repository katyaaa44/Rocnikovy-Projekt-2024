BASEDIR=$(dirname "$0")
echo "Executing program in '$BASEDIR'"

PORT=$1

source $BASEDIR/venv/bin/activate

python $BASEDIR/main.py $PORT
