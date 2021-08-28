# UTN-sensorial-raspberry

Codigo fuente para los raspberry del proyecto Sensorial

Despliegue productivo del proyecto [UTN-sensorial-raspberry-deploy](https://github.com/brianwolf/UTN-sensorial-raspberry-deploy)

![1](img/sensorial.jpg)

---

## Requisitos

* docker 20.10.7
* python 3.9
* virtualenv 20.0.17

## Uso

### Instalacion del ambiente

1. Ejecutar el siguiente comando para crear el ambiente

    ```bash
    make pye
    ```

2. Ingresar en el ambiente generado

    ```bash
    . ./env/bin/activate
    ```

3. Instalar las dependencias con *pip*

    ```bash
    pip install -r requirements.txt
    ```

4. Correr  la app

    ```bash
    python app.py
    ```

### Uso de la API REST

1. Ingresar en la url predefinida
    [http://localhost:5000/](http://localhost:5000/)

2. Para que metodos hay usar la *collection de Postman*
    * Se puede descargar de la api una vez levantada: [http://localhost:5000/postman](http://localhost:5000/postman)
    * o desde el archivo *sensorial-raspberry-v1.X.X.postman_collection.json*

## Repositorio de imagenes

* [dockerhub/sensorial-raspberry](https://hub.docker.com/r/brianwolf94/sensorial-raspberry)

---

## Facultad

![1](img/utn.jpg)

### Referencias

* [Docker builx QEMU](https://stackoverflow.com/questions/67017795/npm-install-is-failing-with-docker-buildx-linux-arm64)
* [Git Actions builx](https://www.docker.com/blog/multi-arch-images/)
* [Git Actions QEMU](https://www.docker.com/blog/multi-arch-images/)
