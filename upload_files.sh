#!/bin/bash

# Definir o caminho local dos arquivos
LOCAL_PATH=~/dev/server/export_framer/exported_pages/*

# Definir o caminho remoto para o servidor EC2
REMOTE_PATH=ec2-user@98.81.238.97:/var/www/html/lucasteoffilo/000links/

# Comando SCP para transferir os arquivos
echo "Iniciando o upload dos arquivos para o servidor..."
scp -i ~/arthificial-key.pem -r $LOCAL_PATH $REMOTE_PATH

# Mensagem de sucesso
if [ $? -eq 0 ]; then
    echo "Arquivos enviados com sucesso!"
else
    echo "Erro ao enviar os arquivos."
fi
