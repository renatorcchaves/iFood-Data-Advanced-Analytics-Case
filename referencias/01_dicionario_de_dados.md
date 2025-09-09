# Dicionário de dados

**Features originais da base de dados**

| Nome da coluna     | Descrição                                                             | Tipo de dado |
|--------------------|-----------------------------------------------------------------------|--------------|
AcceptedCmp1	 	 |1 se o cliente aceitou a oferta na 1ª campanha, 0 caso contrário	     | Numérico     |
AcceptedCmp2		 |1 se o cliente aceitou a oferta na 2ª campanha, 0 caso contrário	     | Numérico     |
AcceptedCmp3		 |1 se o cliente aceitou a oferta na 3ª campanha, 0 caso contrário	     | Numérico     |
AcceptedCmp4		 |1 se o cliente aceitou a oferta na 4ª campanha, 0 caso contrário	     | Numérico     |
AcceptedCmp5		 |1 se o cliente aceitou a oferta na 5ª campanha, 0 caso contrário	     | Numérico     |
Response (target)	 |1 se o cliente aceitou a oferta na última campanha, 0 caso contrário	 | Numérico     |
Complain		     |1 se o cliente reclamou nos últimos 2 anos, 0 caso contrário	         | Numérico     |
DtCustomer		     |data de inscrição do cliente na empresa	                             | Data         |
Education		     |nível de educação do cliente	                                         | Texto        |
Marital		         |estado civil do cliente	                                             | Texto        |
Kidhome		         |número de crianças pequenas na casa do cliente                       	 | Numérico     |
Teenhome		     |número de adolescentes na casa do cliente	                             | Numérico     |
Income		         |renda familiar anual do cliente                                      	 | Numérico     |
MntFishProducts		 |valor gasto em produtos de peixe nos últimos 2 anos	                 | Numérico     |
MntMeatProducts		 |valor gasto em produtos de carne nos últimos 2 anos	                 | Numérico     |
MntFruits		     |valor gasto em frutas nos últimos 2 anos	                             | Numérico     |
MntSweetProducts	 |valor gasto em produtos doces nos últimos 2 anos	                     | Numérico     |
MntWines		     |valor gasto em vinhos nos últimos 2 anos	                             | Numérico     |
MntGoldProds		 |valor gasto em produtos de ouro nos últimos 2 anos	                 | Numérico     |
NumDealsPurchases    |número de compras feitas com desconto	                                 | Numérico     |
NumCatalogPurchases	 |número de compras feitas usando catálogo	                             | Numérico     |
NumStorePurchases	 |número de compras feitas diretamente nas lojas	                     | Numérico     |
NumWebPurchases		 |número de compras feitas pelo site da empresa	                         | Numérico     |
NumWebVisitsMonth    |número de visitas ao site da empresa no último mês	                 | Numérico     |
Recency		         |número de dias desde a última compra                                   | Numérico     |

**Features criadas na etapa de análise exploratória**

| Nome da coluna     | Descrição                                                                             | Tipo de dado |
|--------------------|---------------------------------------------------------------------------------------|--------------|
DaysSinceEnrolled	 | Número de dias desde a inscrição do cliente na base                                   | Numérico     |
YearsSinceEnrolled   | Número de anos desde a inscrição do cliente na base                                   | Numérico     |
Age         		 | Idade do cliente                                                               	     | Numérico     |
MntTotal    		 | Valor gasto em produtos nos ultimos 2 anos (carne, pexe, vinho, fruta, doce, gold)    | Categórico   |
MntRegularProducts   | Valor gasto em produtos regulares nos ultimos 2 anos (exceto GoldProds)	             | Numérico     |
Children             | Total de filhos em casa (criança ou adolecente)                                       | Numérico     |
HasChildren          | Se o cliente possui filhos, independente da quantidade                                | Numérico     |
AcceptedCmpTotal     | Quantidade de ofertas que o cliente aceitou nas campanhas de marketing anteriores     | Numérico     |
HasAcceptedCmp       | 1 se o cliente aceitou alguma oferta na campanhas de marketing, 0 caso contrário      | Numérico     |
NumTotalPurchases    | número total de compras feitas diretamente nas lojas, no site ou no catálogo          | Numérico     |
