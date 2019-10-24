
[[ $_ != $0 ]] && FLAG=1 || FLAG=0

exists()
{
    command -v "$1" >/dev/null 2>&1
}

if ! exists virtualenv ; then
  pip install virtualenv
fi

if ! [ -d env ]; then
  virtualenv --python=/usr/bin/python2.7 env
fi
source env/bin/activate
pip install -r requirements.txt
