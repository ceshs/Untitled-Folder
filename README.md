# WebScraper
Case para Sauter cujo objetivo é capturar dados da Loja de Aplicativos Google Play, para as tentativas foi utilizada a Alexa, da Amazon
A partir dele foi gerado um data frame com os dados obtidos pela função web-scraper (na qual podemos selecionar o aplicativo, a quantidade de reviews puxados, etc) junto do CSV segmentando a avaliação e html com o report. 
Por fim os dados são enviados ao BigQuery e comparados com os ja salvos pelo programa para evitar sem repetição de informações
