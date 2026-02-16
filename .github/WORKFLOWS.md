# GitHub Actions Workflows

This project includes two GitHub Actions workflows for automated CI/CD.

## Workflows

### 1. PR Check (`pr-check.yml`)

**Triggers:** On pull requests to `main` or `develop` branches

**Steps:**
1. ✅ **Checkout** - Checks out the code
2. ✅ **Build** - Sets up Python environment and installs dependencies
3. ✅ **Test** - Runs linting (flake8) and unit tests with coverage
4. ✅ **Docker Build** - Builds Docker image for the PR
5. ✅ **Docker Test** - Tests the Docker image
6. ✅ **Comment** - Posts results to the PR

**Purpose:** Validates pull requests before merging

---

### 2. CI/CD Pipeline (`pr-ci.yml`)

**Triggers:** 
- Push to `main` or `develop` branches
- Manual workflow dispatch

**Jobs:**

#### Job 1: Build and Test
1. ✅ **Checkout** - Checks out the code
2. ✅ **Build** - Sets up Python and installs dependencies
3. ✅ **Test** - Runs linting and tests with coverage
4. ✅ **Upload Coverage** - Uploads coverage to Codecov

#### Job 2: Build Docker
1. ✅ **Checkout** - Checks out the code
2. ✅ **Build Docker Image** - Builds and pushes to Docker Hub
3. ✅ **Test Docker Image** - Validates the built image

#### Job 3: Deploy to Production (main branch only)
1. ✅ **Checkout** - Checks out the code
2. ✅ **Deploy** - Deploys to production server via SSH
3. ✅ **Health Check** - Verifies deployment health
4. ✅ **Rollback** - Automatic rollback on failure

#### Job 4: Deploy to Staging (develop branch only)
1. ✅ **Checkout** - Checks out the code
2. ✅ **Deploy** - Deploys to staging server
3. ✅ **Health Check** - Verifies staging deployment

---

## Required Secrets

Configure these secrets in your GitHub repository:
**Settings → Secrets and variables → Actions → New repository secret**

### Docker Hub Secrets
- `DOCKER_USERNAME` - Your Docker Hub username
- `DOCKER_PASSWORD` - Your Docker Hub password or access token

### Deployment Secrets (Production)
- `DEPLOY_HOST` - Production server hostname/IP
- `DEPLOY_USER` - SSH username for deployment
- `DEPLOY_SSH_KEY` - Private SSH key for authentication
- `DEPLOY_PORT` - SSH port (optional, defaults to 22)
- `PRODUCTION_URL` - Production API URL (e.g., https://api.manchesterseals.com)

### Deployment Secrets (Staging)
- `STAGING_HOST` - Staging server hostname/IP
- `STAGING_URL` - Staging API URL (e.g., https://staging.manchesterseals.com)

---

## Setup Instructions

### 1. Configure Docker Hub

If you want to push Docker images:

```bash
# Login to Docker Hub
docker login

# Create repository: manchesterseals/manchester-seals-api
# Go to: https://hub.docker.com/repository/create
```

Add Docker Hub credentials to GitHub secrets.

### 2. Configure Deployment Servers

**Generate SSH key for deployment:**
```bash
ssh-keygen -t ed25519 -C "github-actions-deployment" -f ~/.ssh/github_deploy
```

**Add public key to servers:**
```bash
# Copy public key
cat ~/.ssh/github_deploy.pub

# On production/staging servers:
echo "PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
```

**Add private key to GitHub secrets:**
```bash
# Copy private key
cat ~/.ssh/github_deploy

# Add to GitHub as DEPLOY_SSH_KEY secret
```

### 3. Configure GitHub Environments

Create environments in GitHub:
**Settings → Environments → New environment**

1. **production**
   - Add protection rules (require approval, specific branches)
   - Add environment secrets if needed

2. **staging**
   - Configure as needed

---

## Testing Workflows Locally

### Test with Act (GitHub Actions locally)

```bash
# Install act
brew install act

# Run PR check workflow
act pull_request -W .github/workflows/pr-check.yml

# Run CI workflow
act push -W .github/workflows/pr-ci.yml
```

---

## Workflow Features

### PR Check Workflow
- ✅ Runs on every PR
- ✅ Fast feedback (5-10 minutes)
- ✅ MongoDB service container
- ✅ Python linting
- ✅ Unit tests with coverage
- ✅ Docker build and test
- ✅ PR comments with results

### CI/CD Workflow
- ✅ Automatic on main/develop push
- ✅ Full test suite
- ✅ Docker Hub integration
- ✅ Multi-environment deployment
- ✅ Health checks
- ✅ Automatic rollback
- ✅ Manual trigger option

---

## Monitoring Workflows

### View Workflow Runs
Go to: `https://github.com/manchesterseals/manchester-seals-python-webservice/actions`

### Check Workflow Status
Badge for README.md:
```markdown
![CI/CD](https://github.com/manchesterseals/manchester-seals-python-webservice/workflows/CI%2FCD%20Pipeline/badge.svg)
```

---

## Customization

### Modify Python Version
Edit workflow files, change:
```yaml
python-version: '3.9'
```

### Change Deployment Method
Replace SSH deployment with:
- AWS ECS
- Google Cloud Run
- Azure App Service
- Heroku
- Kubernetes

### Add Additional Tests
Add steps in workflow:
```yaml
- name: Integration tests
  run: pytest tests/integration -v

- name: Load tests
  run: locust -f tests/load_test.py
```

---

## Troubleshooting

### Workflow Fails on MongoDB Connection
- Ensure MongoDB service is healthy
- Check `MONGO_URI` environment variable
- Verify port 27017 is available

### Docker Push Fails
- Verify `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets
- Check Docker Hub repository exists
- Ensure proper permissions

### Deployment Fails
- Verify SSH key is correct and has proper permissions
- Check server is reachable from GitHub Actions
- Verify docker-compose.yml exists on server
- Check server has docker and docker-compose installed

### Health Check Fails
- Verify API is actually running
- Check health endpoint URL is correct
- Ensure server allows health check requests
- Check for firewall/security group rules

---

## Best Practices

1. **Always run PR checks** before merging
2. **Review workflow logs** for any warnings
3. **Keep secrets secure** - never commit them
4. **Use environment protection** for production
5. **Monitor deployments** and set up alerts
6. **Test locally** before pushing workflow changes
7. **Keep dependencies updated** in workflows

---

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [SSH Deploy Action](https://github.com/appleboy/ssh-action)
- [Codecov Action](https://github.com/codecov/codecov-action)

---

## Workflow Files

- `.github/workflows/pr-check.yml` - PR validation workflow
- `.github/workflows/pr-ci.yml` - Full CI/CD pipeline

Both workflows are production-ready and follow GitHub Actions best practices!

