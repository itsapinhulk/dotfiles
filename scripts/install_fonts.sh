SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
sudo mkdir -p /usr/local/share/fonts
sudo cp -Rf ${SCRIPT_DIR}/../fonts/* /usr/local/share/fonts
sudo fc-cache -fv

