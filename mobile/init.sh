#!/bin/bash

# Verifica si el script se ejecuta con permisos necesarios
if [ "$EUID" -ne 0 ]; then
  echo "Ejecutar con sudo."
  exit
fi

# Detecta el gestor de paquetes
if command -v dnf >/dev/null 2>&1; then
  PKG_MANAGER="dnf"
elif command -v apt >/dev/null 2>&1; then
  PKG_MANAGER="apt"
elif command -v pacman >/dev/null 2>&1; then
  PKG_MANAGER="pacman"
else
  echo "Gestor de paquetes no reconocido. Instala Python 3.10, pip y xclip manualmente."
  exit 1
fi

echo "Gestor de paquetes detectado: $PKG_MANAGER"

# Función para instalar paquetes según el gestor detectado
install_package() {
  case $PKG_MANAGER in
    dnf)
      dnf install -y "$1"
      ;;
    apt)
      apt update && apt install -y "$1"
      ;;
    pacman)
      pacman -Syu --noconfirm "$1"
      ;;
  esac
}

# Elimina la carpeta venv si existe
if [ -d "venv" ]; then
  echo "Eliminando carpeta venv existente..."
  rm -rf venv
fi

# Instalar Python 3.10
echo "Instalando Python 3.10..."
install_package python3.10

# Instalar xclip (necesario para Kivy)
echo "Instalando xclip..."
install_package xclip

# Descarga e instala pip
echo "Descargando e instalando pip..."
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.10 get-pip.py
rm get-pip.py  # Elimina el instalador de pip

# Crea el entorno virtual
echo "Creando entorno virtual..."
python3.10 -m venv venv

# Activa el entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instala las dependencias desde requirements.txt
echo "Instalando dependencias desde requirements.txt..."
if [ ! -f requirements.txt ]; then
  echo "Error: requirements.txt no encontrado."
  deactivate
  exit 1
fi

pip install -r requirements.txt

# Verifica la instalación de cada paquete en requirements.txt
echo "Verificando instalación de paquetes..."
while IFS= read -r package || [ -n "$package" ]; do
  # Ignora líneas en blanco o comentarios
  if [[ "$package" == "" || "$package" == \#* ]]; then
    continue
  fi
  # Extrae el nombre del paquete antes de "=="
  package_name=$(echo "$package" | cut -d= -f1)
  pip show "$package_name" >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "Paquete instalado correctamente: $package_name"
  else
    echo "Error: El paquete $package_name no se instaló correctamente."
  fi
done < requirements.txt

# Verifica la instalación de Kivy específicamente
echo "Verificando instalación de Kivy..."
python -c "import kivy; print('Kivy instalado:', kivy.__version__)"
