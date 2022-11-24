run_mosquitto:
	docker run -p 1883:1883 -v /home/anis/Desktop/mosquitto-test/config/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
build_livello:
	docker build -t livello-challenge client/.
remove_livello:
	docker rmi livello-challenge:latest