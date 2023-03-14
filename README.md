# Simulated PV Photovoltaic


### Installation Guide 

After cloning the project, run these commands in the project root.

```
pip install .
python setup.py clean
```

#### Docker Steps in different terminals

```
docker-compose build

```

For RabbitMQ-Service

```

docker-compose run --name rabbit rabbit

```

For starting the Simulator-Service

```

docker-compose run simulator

```

For starting the Meter-Service

```

docker-compose run meter

```

Get the results in the file

```

docker-compose run simulator cat pv-simulator-output.csv

```







