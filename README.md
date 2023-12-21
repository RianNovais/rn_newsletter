# rn_newsletter
#### Aplicação com objetivo de ser uma newsletter enviando noticias via email, extraidas de sites automaticamente, e também informações completas das noticias via Excel.

#### Application intended to be a newsletter sending news via email, automatically extracted from websites, and also complete information on the news via Excel.

##### ->Captura as principais noticias automaticamente dos sites:
##### ->Catches the main news automatically from the websites:

- https://g1.globo.com/
- https://www.uol.com.br/
- https://www.cnnbrasil.com.br/
- https://www.terra.com.br/noticias/

#### Como usar (how to use)

    1. Mude o arquivo .env-example coloque suas informações de email e senha e renomeie para .env (Change the file .env-example put your email and password information and rename it to .env)
    2. Vá em mail e mude o arquivo recipients.txt colocando os destinatários que você deseja que a newsletter seja enviada. (Go to mail and change the recipients.txt file by entering the recipients you want the newsletter to be sent to.)
    3. Instale os requisitos (Install the requirements.txt)
    4. Execute o arquivo main.py (Run the main.py file)


#### Como funciona ? (How does it work?)

    1. É instanciado um objeto da classe NewsScraper, que vem do arquivo scraper.py, essa classe na sua função __init__, executa alguns métodos que vão em cada site e extrai essas noticias, coloca em um formato de lista de dicionários.  e transformam em um dataframe do pandas. Posteriormente depois de ser pega todas as noticias, e criado um dataframe para cada respectivo site, é executado um método que junta esses dataframes em um dataframe só que irá conter todas as noticias, a partir desse dataframe é executado um método que cria um arquivo .xlsx a partir desse dataframe.
    2. Depois de passar da classe NewsScraper, é instanciado um objeto da classe Email, passando o dataframe da classe anterior, e o caminho do arquivo .xlsx. No método __init__ dessa classe, é feita uma conexão SMTP utilizando o yagmail, com o email que iremos enviar nossa newsletter, essa conexão é feita usando parametros de configuração que vem do arquivo .env. Posteriormente é executado um método para ler os destinatarios no arquivo recipients.txt, depois é executado outro método que cria uma string com todas nossas noticias, e substitui no nosso html template, "content.html", depois no método send_email nosso email é enviado, passando os destinatarios, a conteudo do html, e o nosso arquivo excel.

    1. an object of the NewsScraper class is instantiated, which comes from the scraper.py file, this class in its __init__ function, executes some methods, which go to each site and extract these news items, place them in a dictionary list format and transform them into a pandas dataframe. Later, after all the news has been taken, and a dataframe has been created for each respective site, a method is executed that joins these dataframes into a single dataframe that will contain all the news, from this dataframe a method is executed that creates an .xlsx file from this dataframe.
    2. After passing the NewsScraper class, an object of the Email class is instantiated, passing the dataframe of the previous class, and the path of the .xlsx file. In the __init__ method of this class, an SMTP connection is made using yagmail, with the email address that we are going to send our newsletter to, this connection is made using configuration parameters that come from the .env file. Then a method is executed to read the recipients in the recipients.txt file, then another method is executed that creates a string with all our news, and replaces it in our html template, "content.html", then in the send_email method our email is sent, passing the recipients, the html content, and our excel file.

> Python Version: 3.11
