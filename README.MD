
<h1>checar ip do docker: ip addr show docker0</h1>
<h2>passo 1</h2>
- rodar o docker compose com o comando: docker-compose up
<h2>#Passo 2</h2>
- rodar o script da pasta producer: chmod +x run.sh && ./run.sh
- rodar o script da pasta consummer: chmod +x run.sh && ./run.sh
<h2>#passo 3</h2>
- abrir o navegador 127.0.0.1:5000/docs (caso não funcione, no terminal do producer tem o endereço correto)
<h2>#passo 4</h2>
- instalar o mongodb compass e abrir o banco de dados padrão