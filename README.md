# WorkBox #

Cервис запуска виртуальных сред с использованием инструмента Vagrant

## Сборка и развертывание

### Основное

* проект - [workbox](https://github.com/pr3sto/workbox/tree/master/) / workbox
* скрипты - [workbox](https://github.com/pr3sto/workbox/tree/master/) / scripts

### Сборка

* [Скачать проект](https://github.com/pr3sto/workbox/archive/master.zip)

* Запустить скрипт *make.sh* из папки *scripts*:

```
sudo ./make.sh
```
После этого в папке с проектом будут созданы:

* папка *workboxenv* - папка с виртуальной средой python (virtualenv), с копией проекта;

* deb-пакет *workbox_\<version\>_\<architecture\>.deb* - собранный пакет проекта.

```
/.../downloaded_project
    ├── README.md
    ├── scripts
    │   └── ...
    ├── workbox
    │   └── ...
    ├── workboxenv
    │   └── ...
    └── workbox_<version>_<architecture>.deb
```

### Развертывание

* Установить пакет (будут распакованы файлы проекта, настроен файл */etc/hosts* и добавлен файл конфигурации apache2):

```
sudo dpkg -i workbox_<version>_<architecture>.deb
```

* Настроить схему БД (если сервис устанавливается впервые) с помощью скрипта *setup_mongo_schema.sh*:

```
sudo ./setup_mongo_schema.sh
```

* Установка может прерваться из-за отсутствия зависимостей. Можно установить необходимые зависимости вручную, или с помощью скрипта *install_software.sh* (mongodb и docker необходимо устанавливать вручную). Инструкция по установке [mongodb](https://docs.mongodb.com/manual/administration/install-on-linux/) и [docker](https://docs.docker.com/engine/installation/linux/).

```
sudo ./install_software.sh
```

* Также для установки необходимо, чтобы сервисы mongod и apache2 были запущены. Если какой-то сервис не запущен, будет выведено соответствующее сообщение. Запуск сервисов:

```
sudo service mongod start 
sudo service apache2 start

или

sudo /etc/init.d/mongodb start
sudo /etc/init.d/apache2 start
```

* После успешной установки сервис будет доступен по адресу:

```
http://workbox/
```

* **ВНИМАНИЕ!** Логин и пароль для администратора: *admin*. После установки сервиса необходимо создать настоящий аккаунт для администратора и удалить стандартный.
