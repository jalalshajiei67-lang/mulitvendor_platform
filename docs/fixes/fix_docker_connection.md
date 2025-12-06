# Fix Docker Connection Issue

## Commands to Run in SSH

Try these in order:

### 1. Check if Docker is running
```bash
systemctl status docker
```

### 2. Restart Docker service
```bash
systemctl restart docker
```

### 3. Try docker ps again
```bash
docker ps
```

### 4. If still not working, check your user
```bash
whoami
groups
```

### 5. Try with sudo (even though you're root)
```bash
sudo docker ps
```

### 6. Check Docker socket permissions
```bash
ls -la /var/run/docker.sock
```

### 7. If needed, fix permissions
```bash
chmod 666 /var/run/docker.sock
```

