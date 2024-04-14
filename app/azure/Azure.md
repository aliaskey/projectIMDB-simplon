docker pull ubuntu:22.04
docker run -it ubuntu:22.04
docker build . -t projetimdb
docker run -d --name project_imbd_new -p 8081:5000 projetimdb
PS C:\Users\lemai\Desktop\IMDB\PROJECT-IMBD\app> streamlit run code_API_Streamlit.py --server.port 5000


création et la gestion des conteneurs et de l'application Web App dans Azure :

### Se Connecter à Azure
```bash
az login
```

### Définir l'Abonnement Azure (Si Plusieurs Abonnements Sont Associés à Votre Compte)
```bash
az account set --subscription 4ff70210-fbda-467a-b201-49b212fcda7a
```

### Travailler avec Azure Container Registry (ACR)
```bash
# Connexion à l'ACR
az acr login --name cristelacr

# Activation de l'accès administrateur sur l'ACR
az acr update -n cristelacr --admin-enabled true

# Récupération des identifiants de l'ACR
az acr credential show --name cristelacr

{
  "passwords": [
    {
      "name": "password",
      "value": "vLhxefl/fOee86Y115HmNteZAe1XB2bxWb/RkQiKCu+ACRCGB2zd"
    },
    {
      "name": "password2",
      "value": "/K3EH0NTtHja8KiSiAErAfAN+KYcnX0LIkrlykJOpe+ACRCUhmm6"
    }
  ],
  "username": "cristelacr"
}


# Construction et push de l'image Docker
docker build -t cristelacr.azurecr.io/projetimdb .
docker push cristelacr.azurecr.io/projetimdb
```

### Déploiement de l'Instance de Conteneur Azure
```bash
az container create --resource-group SimplonDevIA --name projetimdbcontainer --image cristelacr.azurecr.io/projetimdb:latest --cpu 1 --memory 1.5 --registry-login-server cristelacr.azurecr.io --registry-username cristelacr --registry-password vLhxefl/fOee86Y115HmNteZAe1XB2bxWb/RkQiKCu+ACRCGB2zd --dns-name-label projetimdb-app --ports 80
```

### Gestion de l'Application Web App dans Azure App Service
```bash
# Création d'un Plan App Service
az appservice plan create --name crisantoIMBDProdPlan --resource-group SimplonDevIA --sku B1 --is-linux

# Création d'une Web App avec une Image Docker
az webapp create --resource-group SimplonDevIA --plan crisantoIMBDProdPlan --name appimdbcrisantovf --deployment-container-image-name cristelacr.azurecr.io/projetimdb:latest

# Configuration des paramètres de l'application Web App
az webapp config appsettings set --name appimdbcrisantovf --resource-group SimplonDevIA --settings WEBSITES_PORT=8501

# Redémarrage de l'application Web App
az webapp restart --name appimdbcrisantovf --resource-group SimplonDevIA

# Consultation des paramètres de configuration
az webapp config appsettings list --name appimdbcrisantovf --resource-group SimplonDevIA

# Suivi des logs en temps réel
az webapp log tail --name appimdbcrisantovf --resource-group SimplonDevIA
```

