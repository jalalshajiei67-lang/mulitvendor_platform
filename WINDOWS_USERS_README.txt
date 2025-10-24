╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                    WINDOWS USERS - QUICK START GUIDE                       ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 FOR WINDOWS USERS - EASIEST DEPLOYMENT METHOD
═══════════════════════════════════════════════════════════════════════════════

🎯 OPTION 1: ONE-CLICK DEPLOYMENT (EASIEST!)
───────────────────────────────────────────────────────────────────────────────

1. Double-click: CHECK_BEFORE_DEPLOY.bat
   → This verifies everything is ready

2. Double-click: DEPLOY_NOW.bat
   → This deploys everything automatically

3. Follow the on-screen instructions

That's it! The batch files do everything for you.


🎯 OPTION 2: MANUAL STEP-BY-STEP
───────────────────────────────────────────────────────────────────────────────

STEP 1: Create Environment File
Open PowerShell or Command Prompt in this folder and run:
  copy env.production .env

STEP 2: Deploy to VPS
Double-click or run:
  deploy-windows.bat

Enter SSH password when prompted: e<c6w:1EDupHjf4*

STEP 3: Setup on VPS
Open PowerShell or Command Prompt and run:
  ssh root@158.255.74.123

Enter password: e<c6w:1EDupHjf4*

Then on the VPS, run:
  cd /opt/multivendor_platform
  chmod +x *.sh
  ./server-deploy.sh

STEP 4: Create Admin User
Still on the VPS, run:
  docker-compose exec backend python manage.py createsuperuser

STEP 5: Access Your Site
Open browser and go to:
  http://158.255.74.123


📁 WINDOWS-SPECIFIC FILES
═══════════════════════════════════════════════════════════════════════════════

✓ DEPLOY_NOW.bat              - One-click deployment
✓ CHECK_BEFORE_DEPLOY.bat     - Pre-deployment verification
✓ deploy-windows.bat           - Main deployment script
✓ WINDOWS_USERS_README.txt    - This file


🛠️ TOOLS YOU MIGHT NEED
═══════════════════════════════════════════════════════════════════════════════

For SSH access, you need an SSH client:

Option 1: Built-in (Windows 10+)
  → PowerShell or CMD already has SSH
  → Just run: ssh root@158.255.74.123

Option 2: PuTTY
  → Download from: https://www.putty.org
  → Use it to connect to 158.255.74.123

Option 3: Windows Terminal (Recommended)
  → Install from Microsoft Store
  → Modern terminal with tabs
  → Has SSH built-in


⚠️ COMMON WINDOWS ISSUES
═══════════════════════════════════════════════════════════════════════════════

Issue: "ssh is not recognized"
Solution: Install OpenSSH or use PuTTY

Issue: "tar is not recognized"
Solution: Windows 10+ has tar built-in. If not, use 7-Zip or WinRAR

Issue: Scripts won't run
Solution: Right-click → "Run as Administrator"

Issue: Files won't upload
Solution: Check firewall isn't blocking the connection


💡 TIPS FOR WINDOWS USERS
═══════════════════════════════════════════════════════════════════════════════

1. Use PowerShell (better than CMD)
   → Right-click Start → "Windows PowerShell"

2. Run scripts from project folder
   → cd C:\Users\F003\Desktop\damirco

3. If SSH prompts are confusing
   → Use PuTTY instead (graphical interface)

4. Keep SSH password handy
   → VPS Password: e<c6w:1EDupHjf4*

5. For file editing
   → Use Notepad++, VS Code, or any text editor
   → Don't use regular Notepad (formatting issues)


📚 DOCUMENTATION
═══════════════════════════════════════════════════════════════════════════════

For detailed information, see these files:

• 🚀_START_HERE_FIRST.txt      - Overall quick start
• START_DEPLOYMENT_HERE.md      - Complete deployment guide
• QUICK_START.md                - 5-minute deployment
• DEPLOYMENT_GUIDE.md           - Comprehensive reference
• QUICK_REFERENCE.md            - Command cheat sheet
• TROUBLESHOOTING_QUICK.md      - Quick problem solving


🎯 RECOMMENDED WORKFLOW FOR WINDOWS
═══════════════════════════════════════════════════════════════════════════════

1. Run: CHECK_BEFORE_DEPLOY.bat
   ✓ Verifies everything is ready

2. Run: DEPLOY_NOW.bat
   ✓ Deploys to VPS

3. Use PowerShell for VPS access:
   ssh root@158.255.74.123

4. On VPS, run:
   cd /opt/multivendor_platform
   chmod +x *.sh
   ./server-deploy.sh

5. Create admin:
   docker-compose exec backend python manage.py createsuperuser

6. Done! Access:
   http://158.255.74.123


🔧 AFTER DEPLOYMENT - MANAGEMENT
═══════════════════════════════════════════════════════════════════════════════

All management is done via SSH on the VPS:

1. Connect: ssh root@158.255.74.123
2. Go to project: cd /opt/multivendor_platform
3. Use interactive menu: ./manage-deployment.sh

OR use individual commands:
  ./health-check.sh           - Check health
  ./monitor.sh                - Monitor system
  ./backup-database.sh        - Backup database
  docker-compose logs -f      - View logs
  docker-compose restart      - Restart services


✅ CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

Before deploying:
□ Ran CHECK_BEFORE_DEPLOY.bat
□ .env file exists
□ Know VPS password (e<c6w:1EDupHjf4*)
□ Can SSH to VPS (tested)

After deploying:
□ All containers running
□ Created superuser
□ Site accessible at http://158.255.74.123
□ Admin panel accessible at http://158.255.74.123/admin
□ Tested basic functionality


🆘 NEED HELP?
═══════════════════════════════════════════════════════════════════════════════

1. Quick problems: TROUBLESHOOTING_QUICK.md
2. Detailed help: DEPLOYMENT_GUIDE.md (Troubleshooting section)
3. Commands: QUICK_REFERENCE.md


═══════════════════════════════════════════════════════════════════════════════
                             READY TO DEPLOY!
═══════════════════════════════════════════════════════════════════════════════

→ Run: CHECK_BEFORE_DEPLOY.bat
→ Then: DEPLOY_NOW.bat

That's it! Everything else is automatic.

═══════════════════════════════════════════════════════════════════════════════

