# COVID IN BRASIL DASHBOARD

---
## OBJETIVO:
Esse projeto busca mostrar dados da pandemia da COVID-19 no Brasil de forma simples e intuitiva.
A partir desse dashboard, você será capaz de avaliar as dados a nível nacional e estadual sobre número de casos e mortes devidas ao vírus, além de poder checar os dados de datas específicas.

---
## DOS PRECEDENTES:
De início, é preciso ressaltar que este não é um projeto 100% autoral. Ele surge do interesse da plataforma de cursos Asimov Academy de fomentar o mercado de análise de dados a parti de um projeto desafiador. Meu interesse pela área e a complexidade o projeto me levaram a aceitar o desafio e torná-lo o projeto a ser apresentado na faculdade. Todos os créditos de autoria à Asimov Academy. 

---
## TECNOLOGIAS UTILIZADAS:
* Python
  * Dash
  * Plotly
  * PIL
  * Pandas
  * Json

---
## GUIA DE USO:
### Da execução:
1. É necessário baixar todos os arquivos do repositório e colocá-los na mesma pasta para o perfeito funcionamneto da aplicação;
2. Após baixar todos os arquivos, execute o arquivo "dashboard.py";
3. No seu terminal, será gerado um link baseado em endereço IP. Esse será o localhost onde a aplicação será hospedada;
4. Abra o link ou de forma direta como seu editor de código sugerir ou copie o link e cole-o na barra de busca do seu navegador;

### Do uso:
1. Inicialmente, o dashboard mostrará os dados acumuladas até a data 13/05/2021, na barra lateral esquerda a nível nacional e a nível estadual na direita;
2. É possível visualizar dados a nível estadual clicando no território da UF no mapa e posicionando o cursor sobre seu território;
3. Para voltar a ver dados a nível nacional basta clicar no botão localizado na parte superior da barra lateral esquerda;
4. Quanto mais próximo do vermelho intenso estiver a cor da UF, mais casos acumulados ela terá na data selecionada;
5. O dashboard disponibiliza dados relativos ao período 25/02/2020 - 13/05/2021;
6. Ao selecionar uma data a partir do seletor abaixo do botão azul, é possível ver as informações acumuladas até a data selecionada;
7. Utilizando o menu em dropdown, é possível visulizar 4 dados:
   * Casos acumulados até a data selecionada;
   * Novos casos na data selecionada (Opção pré-selecionada);
   * Total de mortes até a data selecionada;
   * Mortes por dia até a data selecionada;
