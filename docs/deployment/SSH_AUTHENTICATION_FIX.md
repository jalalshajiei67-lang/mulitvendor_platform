# SSH Authentication Fix for GitHub Actions

## Error Message
```
ssh: handshake failed: ssh: unable to authenticate, attempted methods [none publickey], no supported methods remain
```

## Root Cause
This error occurs when GitHub Actions cannot authenticate to your VPS using SSH. The most common causes are:

1. **SSH key not properly configured in GitHub Secrets**
2. **Public key not in server's authorized_keys**
3. **Incorrect SSH key format**
4. **Wrong username or host**

## Step-by-Step Fix

### Step 1: Verify GitHub Secrets

Go to your GitHub repository:
1. **Settings** → **Secrets and variables** → **Actions**
2. Verify these secrets exist:
   - `VPS_HOST` - Should be your VPS IP (e.g., `185.208.172.76`)
   - `VPS_USER` - Should be your SSH username (e.g., `root` or `deploy`)
   - `VPS_SSH_KEY` - Should be your **private** SSH key content

### Step 2: Generate SSH Key (if needed)

If you don't have an SSH key pair:

```bash
# Generate new SSH key (on your local machine)
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_actions_deploy

# This creates:
# - ~/.ssh/github_actions_deploy (private key - for GitHub Secret)
# - ~/.ssh/github_actions_deploy.pub (public key - for VPS)
```

### Step 3: Add Public Key to VPS

**Option A: Using ssh-copy-id (easiest)**
```bash
ssh-copy-id -i ~/.ssh/github_actions_deploy.pub root@185.208.172.76
```

**Option B: Manual copy**
```bash
# 1. Copy public key content
cat ~/.ssh/github_actions_deploy.pub

# 2. SSH to your VPS
ssh root@185.208.172.76

# 3. On VPS, add public key to authorized_keys
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "PASTE_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### Step 4: Add Private Key to GitHub Secrets

1. **Copy private key content:**
   ```bash
   cat ~/.ssh/github_actions_deploy
   ```

2. **In GitHub:**
   - Go to **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `VPS_SSH_KEY`
   - Value: Paste the **entire** private key content, including:
     - `-----BEGIN OPENSSH PRIVATE KEY-----` (or `-----BEGIN RSA PRIVATE KEY-----`)
     - All the key content
     - `-----END OPENSSH PRIVATE KEY-----` (or `-----END RSA PRIVATE KEY-----`)

### Step 5: Verify SSH Key Format

The private key in GitHub Secrets should:
- ✅ Start with `-----BEGIN` and end with `-----END`
- ✅ Include all lines (no truncation)
- ✅ Have no extra spaces or line breaks
- ✅ Be the **private** key (not the public key)

### Step 6: Test SSH Connection Manually

Test from your local machine:
```bash
ssh -i ~/.ssh/github_actions_deploy root@185.208.172.76
```

If this works, the GitHub Actions should also work.

### Step 7: Verify VPS User and Path

Check that the username and path in the workflow match your VPS:

**In `.github/workflows/docker-deploy.yml`:**
```yaml
username: ${{ secrets.VPS_USER }}  # Should match the user you added the key to
script: |
  cd /home/deploy/docker-deploy  # Should match your actual project path
```

**Common paths:**
- `/home/deploy/docker-deploy`
- `/root/docker-deploy`
- `/home/your-username/docker-deploy`

## Alternative: Use Password Authentication (Less Secure)

If SSH keys are problematic, you can use password authentication:

```yaml
- name: Deploy to VPS
  uses: appleboy/ssh-action@v1.0.3
  with:
    host: ${{ secrets.VPS_HOST }}
    username: ${{ secrets.VPS_USER }}
    password: ${{ secrets.VPS_PASSWORD }}  # Instead of key
```

⚠️ **Warning:** Password authentication is less secure than SSH keys.

## Troubleshooting Checklist

- [ ] `VPS_HOST` secret is set and correct
- [ ] `VPS_USER` secret matches the user on VPS
- [ ] `VPS_SSH_KEY` secret contains the **private** key (not public)
- [ ] Private key includes BEGIN and END lines
- [ ] Public key is in `~/.ssh/authorized_keys` on VPS
- [ ] `authorized_keys` has correct permissions (600)
- [ ] `~/.ssh` directory has correct permissions (700)
- [ ] SSH connection works manually from local machine
- [ ] Project path in workflow matches actual path on VPS

## Common Mistakes

1. **Using public key instead of private key** in GitHub Secrets
2. **Truncated key** - missing BEGIN/END lines or middle content
3. **Wrong user** - key added to one user but workflow uses different user
4. **Wrong path** - project directory doesn't exist on VPS
5. **Permissions** - `authorized_keys` or `~/.ssh` have wrong permissions

## Still Having Issues?

1. Check GitHub Actions logs for more details (with `debug: true` enabled)
2. Test SSH manually: `ssh -v -i ~/.ssh/your_key user@vps-ip` (verbose mode)
3. Check VPS SSH logs: `tail -f /var/log/auth.log` (on Ubuntu/Debian)
4. Verify SSH service is running: `systemctl status ssh` or `systemctl status sshd`

