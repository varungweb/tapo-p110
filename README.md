# tapo-p110

## Git clone
```bash
git clone https://github.com/varungweb/tapo-p110.git
cd tapo-p110
```
## Update Creds inside docker compose Environment Variables
```bash
TAPO_USERNAME: "example@mail.com"
TAPO_PASSWORD: "password"
IP_ADDRESS: "192.168.x.x"
```

## Run Inside Docker
```bash
docker compose up -d --build
```

## Access Locally
```bash
http://localhost:8000
```

