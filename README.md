# Project 6: Use GitHub Secrets for Secure Credentials

This project demonstrates how to **securely manage credentials** in GitHub Actions by using **GitHub Secrets**.  
We build and containerize a simple Flask app, push the image to DockerHub, and then deploy it automatically to an **AWS EC2 (Ubuntu)** instance via SSH — all without exposing sensitive data in code.

---

## 🚀 Features
- Flask web app (`app.py`)  
- Dockerized with a lightweight `Dockerfile`  
- GitHub Actions workflow that:  
  - Builds Docker image  
  - Pushes to DockerHub  
  - Deploys app on AWS EC2 instance via SSH  
- Credentials handled using **GitHub Secrets**  

---

## 📂 Project Structure
GitHub-Secrets/
│── app.py
│── requirements.txt
│── Dockerfile
│── README.md
│
└── .github/
└── workflows/
└── deploy-with-secrets.yml


---

## ⚙️ GitHub Actions Workflow
The workflow runs on every push to `main`:
- **Build & Push** → Docker image is built and uploaded to DockerHub.  
- **Deploy** → EC2 instance pulls the new image and restarts the container.  

Example snippet:

```yaml
- name: Log in to Docker Hub
  uses: docker/login-action@v2
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}

- name: Deploy to EC2
  uses: appleboy/ssh-action@v0.1.6
  with:
    host: ${{ secrets.EC2_HOST }}
    username: ${{ secrets.EC2_USER }}
    key: ${{ secrets.EC2_SSH_KEY }}
    script: |
      sudo docker pull ${{ secrets.DOCKER_USERNAME }}/github-secrets-app:latest
      sudo docker stop gh-secrets-app || true
      sudo docker rm gh-secrets-app || true
      sudo docker run -d --name gh-secrets-app -p 80:5000 --restart unless-stopped \
        ${{ secrets.DOCKER_USERNAME }}/github-secrets-app:latest
🔑 Required GitHub Secrets

Set the following secrets under: Repo → Settings → Secrets and variables → Actions

DOCKER_USERNAME → DockerHub username
DOCKER_PASSWORD → DockerHub Access Token
EC2_HOST → Public IP of your EC2 instance
EC2_USER → ubuntu (for Ubuntu AMIs)
EC2_SSH_KEY → Private key (.pem file) content for EC2 login

🖥️ Run Locally (Optional)
To test before pushing:
# Build image
docker build -t github-secrets-app .

# Run container
docker run -p 5000:5000 github-secrets-app

🌍 Access on AWS

After a successful GitHub Actions run, open:
http://<EC2_PUBLIC_IP>

You should see:

Hello from Project 6 - secured with GitHub Secrets!
