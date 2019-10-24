
[[ $_ != $0 ]] && FLAG=1 || FLAG=0

exists()
{
    command -v "$1" >/dev/null 2>&1
}

if [ "$FLAG" != '0' ]; then
    echo "Execute with \"source <file_name>\""
else
  if exists Rscript ; then
      if ! exists virtualenv ; then
          pip3 install virtualenv || pip install virtualenv
      fi
      if ! [ -d ENV ]; then
          virtualenv ENV
      fi
      source ENV/bin/activate
      pip install -r requirements.txt
  else
      echo "Your system does not have R, please install!"
  fi

fi
