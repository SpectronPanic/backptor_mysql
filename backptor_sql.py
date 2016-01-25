#!/usr/bin/env python3.5
# -*- coding: utf-8 -*


import subprocess
from datetime import date, timedelta
import logging
import logging.config
from configparser import ConfigParser
import os

__author__ = 'SpectronPanic'
__copyright__ = 'Copyright 2015'
__credits__ = ['SpectronPanic']
__license__ = 'Open Source'
__version__ = '1.0.0'
__maintainer__ = 'SpectronPanic, KernelPanic'
__email__ = 'fj.leite@yahoo.com, kernelpanic2015@gmail.com'
__status__ = 'Development'


cfg_file = '/home/user/python_codes/cfg/mysql.cfg'
logging.config.fileConfig(cfg_file)
cfg = ConfigParser()
cfg.read(cfg_file)


user = cfg.get('mysql', 'user')
senha = cfg.get('mysql', 'password')
local = cfg.get('mysql', 'mysql_destino')
host = cfg.get('mysql', 'host')
banco = cfg.get('config', 'bancos').split(',')
# diretório de saída
origem = cfg.get('config', 'origem')
# diretório de destino
destino = cfg.get('config', 'destino')
# nome que vem antes da data atual inclusa no final do nome do arquivo
pre_nome = cfg.get('config', 'pre_nome')
# data atual
data_atual = date.today()


def backup_bancos(): #roda o for criando arquivos de backup dos bancos especificados na lista dentro do cfg
    try:
        for x in banco:
            pack = subprocess.Popen(['mysqldump --login-path=local -e "'+x+'" > '
                                     +local+x+'.sql'],
                                    shell=True, stdout=subprocess.PIPE)
            if pack.wait() == 0:
                logging.info("backup_bancos: Backup da tabela %s feito com sucesso!", x)
            else:
                logging.error("backup_bancos: backup_banco = Error %s", pack.wait())
    except Exception as e:
        logging.error("backup_banco: erro: %s", e)


def backup_sqlpack()  #função que pega a pasta onde o backup dos bancos foram feitos e a compacta com a data atual
    data_atual_formatada = data_atual.strftime('%d%m%Y')
    filename = pre_nome+str(data_atual_formatada)+'.tar'
    try:
        pack = subprocess.Popen(['tar', '--overwrite', '-Jcf',
                                 destino+filename, origem], stdout=subprocess.PIPE)
        if pack.wait() == 0:
            logging.info("backup_pack: Backup feito com sucesso!; %s", filename)
        else:
            logging.error("backup_pack: backup_pack = Error %s", pack.wait())
    except Exception as e:
        logging.error("backup_pack: erro: %s", e)


backup_bancos()
backup_sqlpack()
