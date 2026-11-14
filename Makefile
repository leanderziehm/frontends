p c podman-run:
	podman build -t frontends . && podman run -p 8100:8100 frontends

g gen:
	python src/generate_index.py
# 	python -m src.generate_index


# 	podman build -t frontends . && podman run --rm -it -v ssh_data:/app/data -p 8100:8100 frontends
# 	podman build --cgroup-manager cgroupfs -t frontends . && podman run --rm -it -v ssh_data:/app/data -p 8100:8100 frontends
# 	podman build -t frontends . && podman run --rm -it -v ssh_data:/app/data -p 8100:8100 frontends