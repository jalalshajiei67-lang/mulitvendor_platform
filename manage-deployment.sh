#!/bin/bash

# Deployment Management Script
# Easy-to-use interface for common deployment tasks

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

show_menu() {
    clear
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  Multivendor Deployment Manager       ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}What would you like to do?${NC}"
    echo ""
    echo "  1) Start all services"
    echo "  2) Stop all services"
    echo "  3) Restart all services"
    echo "  4) View logs (all services)"
    echo "  5) View logs (backend only)"
    echo "  6) View logs (frontend only)"
    echo "  7) View container status"
    echo "  8) Run Django migrations"
    echo "  9) Collect static files"
    echo "  10) Create Django superuser"
    echo "  11) Access Django shell"
    echo "  12) Access database"
    echo "  13) Backup database"
    echo "  14) Rebuild all containers"
    echo "  15) Clean up (remove unused images)"
    echo "  16) Show resource usage"
    echo "  0) Exit"
    echo ""
    echo -n "Enter your choice: "
}

start_services() {
    echo -e "\n${YELLOW}Starting services...${NC}"
    docker-compose up -d
    echo -e "${GREEN}✓ Services started${NC}"
    sleep 2
}

stop_services() {
    echo -e "\n${YELLOW}Stopping services...${NC}"
    docker-compose down
    echo -e "${GREEN}✓ Services stopped${NC}"
    sleep 2
}

restart_services() {
    echo -e "\n${YELLOW}Restarting services...${NC}"
    docker-compose restart
    echo -e "${GREEN}✓ Services restarted${NC}"
    sleep 2
}

view_logs_all() {
    echo -e "\n${YELLOW}Showing all logs (Press Ctrl+C to exit)...${NC}"
    sleep 2
    docker-compose logs -f
}

view_logs_backend() {
    echo -e "\n${YELLOW}Showing backend logs (Press Ctrl+C to exit)...${NC}"
    sleep 2
    docker-compose logs -f backend
}

view_logs_frontend() {
    echo -e "\n${YELLOW}Showing frontend logs (Press Ctrl+C to exit)...${NC}"
    sleep 2
    docker-compose logs -f frontend
}

view_status() {
    echo -e "\n${YELLOW}Container Status:${NC}"
    docker-compose ps
    echo ""
    read -p "Press Enter to continue..."
}

run_migrations() {
    echo -e "\n${YELLOW}Running Django migrations...${NC}"
    docker-compose exec backend python manage.py migrate
    echo -e "${GREEN}✓ Migrations completed${NC}"
    sleep 2
}

collect_static() {
    echo -e "\n${YELLOW}Collecting static files...${NC}"
    docker-compose exec backend python manage.py collectstatic --noinput
    echo -e "${GREEN}✓ Static files collected${NC}"
    sleep 2
}

create_superuser() {
    echo -e "\n${YELLOW}Creating Django superuser...${NC}"
    docker-compose exec backend python manage.py createsuperuser
    sleep 2
}

django_shell() {
    echo -e "\n${YELLOW}Opening Django shell...${NC}"
    docker-compose exec backend python manage.py shell
}

access_database() {
    echo -e "\n${YELLOW}Accessing database...${NC}"
    docker-compose exec db psql -U postgres -d multivendor_db
}

backup_database() {
    echo -e "\n${YELLOW}Creating database backup...${NC}"
    BACKUP_FILE="backup-$(date +%Y%m%d-%H%M%S).sql"
    docker-compose exec db pg_dump -U postgres multivendor_db > "$BACKUP_FILE"
    echo -e "${GREEN}✓ Database backed up to: $BACKUP_FILE${NC}"
    sleep 2
}

rebuild_containers() {
    echo -e "\n${YELLOW}Rebuilding all containers...${NC}"
    echo -e "${RED}Warning: This will stop all services and rebuild from scratch${NC}"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down
        docker-compose up -d --build
        echo -e "${GREEN}✓ Containers rebuilt${NC}"
    else
        echo -e "${YELLOW}Cancelled${NC}"
    fi
    sleep 2
}

cleanup() {
    echo -e "\n${YELLOW}Cleaning up unused Docker images...${NC}"
    docker system prune -f
    echo -e "${GREEN}✓ Cleanup completed${NC}"
    sleep 2
}

show_resources() {
    echo -e "\n${YELLOW}Resource Usage:${NC}"
    echo ""
    docker stats --no-stream
    echo ""
    echo -e "${YELLOW}Disk Usage:${NC}"
    df -h | grep -E '^Filesystem|/$'
    echo ""
    echo -e "${YELLOW}Memory Usage:${NC}"
    free -h
    echo ""
    read -p "Press Enter to continue..."
}

# Main loop
while true; do
    show_menu
    read choice
    
    case $choice in
        1) start_services ;;
        2) stop_services ;;
        3) restart_services ;;
        4) view_logs_all ;;
        5) view_logs_backend ;;
        6) view_logs_frontend ;;
        7) view_status ;;
        8) run_migrations ;;
        9) collect_static ;;
        10) create_superuser ;;
        11) django_shell ;;
        12) access_database ;;
        13) backup_database ;;
        14) rebuild_containers ;;
        15) cleanup ;;
        16) show_resources ;;
        0) 
            echo -e "\n${GREEN}Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "\n${RED}Invalid option. Please try again.${NC}"
            sleep 2
            ;;
    esac
done



