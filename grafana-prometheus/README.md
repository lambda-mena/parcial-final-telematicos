# Punto 3 Prometheus y Node Exporter
Se decidio realizar este punto usando docker por la facilidad de implementar los servicios
que contienen estos 2 aplicativos, Prometheus será desplegado con un archivo de configuración
que nos permitira definir los jobs que esta esta ingestando, siendo uno de ellos el servicio
de node-exporter que esta exportando la información del nodo (La maquina de Vagrant),
esta información del nodo contiene mediciones sobre el CPU, RAM Disponible y Disco duro.

Archivo prometheus.yml
```
global:
  scrape_interval:     15s 
  evaluation_interval: 15s 

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
    - targets: ['prometheus:9090']

  - job_name: 'node_exporter'
    static_configs:
    - targets: ['node_exporter:9100']
```
El archivo define el intervalo en el cual se scrapea la información de los trabajos
y también el intervalo en el cual se evaluan las alertas, en este caso contamos
con 2 archivos de configuraciones teniendo uno la información del propio prometheus
que normalmente estaríamos hablando de información de su entorno de Golang y en otra
configuración va la configuración al scrapear el node_exporter con la información del nodo.

```
  prometheus:
    image: prom/prometheus
    container_name: prometheus
    restart: unless-stopped
    volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
    - prometheus-data:/prometheus
    ports:
    - 9090:9090
    command:
    - '--config.file=/etc/prometheus/prometheus.yml'
    - '--storage.tsdb.path=/prometheus'
    - '--storage.tsdb.retention.time=1y'
    - '--web.enable-lifecycle'

  node_exporter:
    image: quay.io/prometheus/node-exporter:latest
    container_name: node_exporter
    restart: unless-stopped
    pid: host
    ports:
    - 9100:9100
    command:
      - '--path.rootfs=/host'
    volumes:
     - '/:/host:ro,rslave'
```
En el archivo de docker-compose podemos ver directivas interesantes cómo los comandos en prometheus
que tienen la función de definir configuraciónes para la base de datos que contiene prometheus
siendo tsdb, y el archivo de configuración que leera.

Mientras que para el node-exporter es importante notar que el PID se ejecutara cómo HOST y los volumenes
los cuales poseera sera la información de la maquina entera, esto es importante porque si no fuera así
la información que podría proveer el node-exporter sería la del contenedor y no de la maquina host.

Para levantar los servicios es tan fácil cómo realizar el comando
```bash
sudo docker compose up -d
```

# Punto 4 - Grafana con Prometheus y Node Exporter
Para grafana a si mismo se levanto la versión OSS en un docker, el cual esta exponiendo el puerto 3000
con credenciales admin:admin que nos dejara entrar y configurar los paneles, el data source de prometheus
y otras herramientas cómo los puntos de contacto.

Para acceder al Grafana podemos dirigirnos a 192.168.50.2:3000 para visualizar el aplicativo web y entrar
cómo usuario: admin y contraseña: admin, aquí podremos ver que el grafana no contendra nada, a lo cual
nos tocará dirigirnos al apartado de Conexiones y añadir una nueva Fuente de Datos cómo lo es prometheus
y poner la dirección URL: http://prometheus:9090 con esto ya podremos ir a Dashboards y crear nuestros
dashboards personalizados.

Por si desea tener un dashboard preconfigurado con el cual ver información de su nodo, le recomendamos importar
el dashboard que esta en esta misma carpeta con el nombre "1860_rev37.json", así mismo si un día gustaría de compartir
un panel a un compañero podría hacerlo exportando su modelo.json para que este pueda importarlo
en su grafana.
