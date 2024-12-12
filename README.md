# colortap-api

## Game Backend Setup

### Prerequisites
- Docker
- Docker Compose

### Running the Application
```bash
docker-compose up --build
```
### Down and prune volume
```bash
docker-compose down --volumes
docker system prune --volumes
```

### Accessing the Application
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- PgAdmin: http://localhost:5050

### Environment Variables
Create a `.env` file with:
```
DATABASE_URL=postgresql://gameuser:gamepassword@db:5432/gamedb
```