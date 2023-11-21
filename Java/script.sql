DROP TABLE AUDITOR CASCADE CONSTRAINTS;

DROP TABLE CLASSIFICACAO CASCADE CONSTRAINTS;

DROP TABLE GRAVIDADE CASCADE CONSTRAINTS;

DROP TABLE PACIENTE CASCADE CONSTRAINTS;

DROP TABLE SINAL CASCADE CONSTRAINTS;

DROP SEQUENCE AUDITOR_ID_SEQ;

DROP SEQUENCE CLASSIFICACAO_ID_SEQ;

DROP SEQUENCE GRAVIDADE_ID_SEQ;

DROP SEQUENCE PACIENTE_ID_SEQ;

DROP SEQUENCE SINAL_ID_SEQ;

-- create sequence for id
CREATE SEQUENCE AUDITOR_ID_SEQ
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE CLASSIFICACAO_ID_SEQ
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE GRAVIDADE_ID_SEQ
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE PACIENTE_ID_SEQ
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE SINAL_ID_SEQ
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE TABLE AUDITOR (
	ID_AUDITOR INTEGER DEFAULT AUDITOR_ID_SEQ.NEXTVAL,
	NOME VARCHAR2(50 CHAR) NOT NULL,
	CPF VARCHAR2(11 CHAR) NOT NULL,
	CRM VARCHAR2(20 CHAR),
	COREN VARCHAR2(20 CHAR),
	ESPECIALIDADE VARCHAR2(50 CHAR)
);

ALTER TABLE AUDITOR ADD CONSTRAINT AUDITOR_PK PRIMARY KEY ( ID_AUDITOR );

CREATE TABLE CLASSIFICACAO (
	ID_CLASSIFICACAO INTEGER DEFAULT CLASSIFICACAO_ID_SEQ.NEXTVAL,
	DATA_HORA_CLASSIFICACAO DATE NOT NULL,
	GRAVIDADE_ID_GRAVIDADE INTEGER NOT NULL,
	SINAL_ID_SINAL INTEGER NOT NULL,
	PACIENTE_ID_PACIENTE INTEGER NOT NULL,
	AUDITOR_ID_AUDITOR INTEGER NOT NULL
);

ALTER TABLE CLASSIFICACAO ADD CONSTRAINT CLASSIFICACAO_RISCO_PK PRIMARY KEY ( ID_CLASSIFICACAO );

CREATE TABLE GRAVIDADE (
	ID_GRAVIDADE INTEGER DEFAULT GRAVIDADE_ID_SEQ.NEXTVAL,
	NOME_GRAVIDADE VARCHAR2(20 CHAR) NOT NULL,
	NOME_COR VARCHAR2(20 CHAR) NOT NULL,
	HEXADECIMAL_COR VARCHAR2(6 CHAR)
);

ALTER TABLE GRAVIDADE ADD CONSTRAINT GRAVIDADE_PK PRIMARY KEY ( ID_GRAVIDADE );

CREATE TABLE PACIENTE (
	ID_PACIENTE INTEGER DEFAULT PACIENTE_ID_SEQ.NEXTVAL,
	NOME VARCHAR2(50 CHAR),
	CPF VARCHAR2(11 CHAR),
	RG VARCHAR2(9 CHAR),
	DATA_HORA_ENTRADA DATE NOT NULL,
	DATA_HORA_SAIDA DATE,
	SEXO VARCHAR2(1 CHAR),
	IDADE INTEGER,
	ALTURA INTEGER,
	PESO NUMBER
);

ALTER TABLE PACIENTE ADD CONSTRAINT PACIENTE_PK PRIMARY KEY ( ID_PACIENTE );

CREATE TABLE SINAL (
	ID_SINAL INTEGER DEFAULT SINAL_ID_SEQ.NEXTVAL,
	NOME VARCHAR2(60 CHAR) NOT NULL,
	DESCRICAO VARCHAR2(700 CHAR)
);

ALTER TABLE SINAL ADD CONSTRAINT SINAL_APRESENTADO_PK PRIMARY KEY ( ID_SINAL );

ALTER TABLE CLASSIFICACAO ADD CONSTRAINT CLASSIFICACAO_AUDITOR_FK FOREIGN KEY ( AUDITOR_ID_AUDITOR ) REFERENCES AUDITOR ( ID_AUDITOR );

ALTER TABLE CLASSIFICACAO ADD CONSTRAINT CLASSIFICACAO_GRAVIDADE_FK FOREIGN KEY ( GRAVIDADE_ID_GRAVIDADE ) REFERENCES GRAVIDADE ( ID_GRAVIDADE );

ALTER TABLE CLASSIFICACAO ADD CONSTRAINT CLASSIFICACAO_PACIENTE_FK FOREIGN KEY ( PACIENTE_ID_PACIENTE ) REFERENCES PACIENTE ( ID_PACIENTE);

ALTER TABLE CLASSIFICACAO ADD CONSTRAINT CLASSIFICACAO_SINAL_FK FOREIGN KEY ( SINAL_ID_SINAL ) REFERENCES SINAL ( ID_SINAL );

INSERT INTO AUDITOR (
	NOME,
	CPF,
	CRM,
	COREN,
	ESPECIALIDADE
) VALUES (
	'Antonieta Franco de Andrade',
	'12345678901',
	'15105',
	NULL,
	'Cardiologista'
);

INSERT INTO AUDITOR (
	NOME,
	CPF,
	CRM,
	COREN,
	ESPECIALIDADE
) VALUES (
	'Luis Campos',
	'74114395091',
	'13660',
	NULL,
	'Neurologista'
);

INSERT INTO AUDITOR (
	NOME,
	CPF,
	CRM,
	COREN,
	ESPECIALIDADE
) VALUES (
	'Tábata Ávila de Angola',
	'08946245042',
	'93834',
	NULL,
	'Ortopedista'
);

INSERT INTO AUDITOR (
	NOME,
	CPF,
	CRM,
	COREN,
	ESPECIALIDADE
) VALUES (
	'Mateus Cleberson de Bittencourt Neto',
	'38092133069',
	'93667',
	NULL,
	'Oftalmologista'
);

INSERT INTO AUDITOR (
	NOME,
	CPF,
	CRM,
	COREN,
	ESPECIALIDADE
) VALUES (
	'Lívia Talita Bezerra',
	'96277197061',
	'18860',
	NULL,
	'Otorrinolaringologista'
);

INSERT INTO AUDITOR (
	NOME,
	CPF,
	CRM,
	COREN,
	ESPECIALIDADE
) VALUES (
	'Manuel Filipe Cruz',
	'67269498040',
	'70118',
	NULL,
	'Pneumologista'
);

INSERT INTO AUDITOR (
	NOME,
	CPF,
	CRM,
	COREN,
	ESPECIALIDADE
) VALUES (
	'João Aragão de Fonseca',
	'47678397003',
	'27936',
	NULL,
	'Psiquiatra'
);

INSERT INTO AUDITOR (
	NOME,
	CPF,
	CRM,
	COREN,
	ESPECIALIDADE
) VALUES (
	'Giovane Dominato de Ferreira',
	'38137578030',
	'47427',
	NULL,
	'Radiologista'
);

INSERT INTO AUDITOR (
	NOME,
	CPF,
	CRM,
	COREN,
	ESPECIALIDADE
) VALUES (
	'Isabella Sabrina de Ferminiano',
	'55262749003',
	'65593',
	NULL,
	'Urologista'
);

INSERT INTO AUDITOR (
	NOME,
	CPF,
	CRM,
	COREN,
	ESPECIALIDADE
) VALUES (
	'Andres Faria Grego',
	'17264754090',
	'78029',
	NULL,
	'Ginecologista'
);

-- Protoclo Manchester é dividido em 5 gravidades, por isso a tabela possui apenas 5 linhas
INSERT INTO GRAVIDADE (
	NOME_GRAVIDADE,
	NOME_COR,
	HEXADECIMAL_COR
) VALUES (
	'EMERGÊNCIA',
	'Vermelho',
	'FF0000'
);

INSERT INTO GRAVIDADE (
	NOME_GRAVIDADE,
	NOME_COR,
	HEXADECIMAL_COR
) VALUES (
	'MUITO URGENTE',
	'Laranja',
	'FFA500'
);

INSERT INTO GRAVIDADE (
	NOME_GRAVIDADE,
	NOME_COR,
	HEXADECIMAL_COR
) VALUES (
	'URGENTE',
	'Amarelo',
	'FFFF00'
);

INSERT INTO GRAVIDADE (
	NOME_GRAVIDADE,
	NOME_COR,
	HEXADECIMAL_COR
) VALUES (
	'POUCO URGENTE',
	'Verde',
	'00FF00'
);

INSERT INTO GRAVIDADE (
	NOME_GRAVIDADE,
	NOME_COR,
	HEXADECIMAL_COR
) VALUES (
	'NÃO URGENTE',
	'Azul',
	'0000FF'
);

INSERT INTO PACIENTE (
	NOME,
	CPF,
	RG,
	DATA_HORA_ENTRADA,
	DATA_HORA_SAIDA,
	SEXO,
	IDADE,
	ALTURA,
	PESO
) VALUES (
	'Breno Gonçalves de Pascoal',
	'59450357005',
	'322135205',
	TO_DATE('2021-05-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'),
	TO_DATE('2021-05-01 10:30:00', 'YYYY-MM-DD HH24:MI:SS'),
	'M',
	30,
	180,
	80
);

INSERT INTO PACIENTE (
	NOME,
	CPF,
	RG,
	DATA_HORA_ENTRADA,
	DATA_HORA_SAIDA,
	SEXO,
	IDADE,
	ALTURA,
	PESO
) VALUES (
	NULL,
	NULL,
	NULL,
	TO_DATE('2021-05-01 10:01:00', 'YYYY-MM-DD HH24:MI:SS'),
	NULL,
	NULL,
	NULL,
	NULL,
	NULL
);

INSERT INTO PACIENTE (
	NOME,
	CPF,
	RG,
	DATA_HORA_ENTRADA,
	DATA_HORA_SAIDA,
	SEXO,
	IDADE,
	ALTURA,
	PESO
) VALUES (
	'Laura Domingues',
	'79728326092',
	'388284225',
	TO_DATE('2022-12-01 10:30:20', 'YYYY-MM-DD HH24:MI:SS'),
	NULL,
	'F',
	12,
	168,
	50
);

INSERT INTO PACIENTE (
	NOME,
	CPF,
	RG,
	DATA_HORA_ENTRADA,
	DATA_HORA_SAIDA,
	SEXO,
	IDADE,
	ALTURA,
	PESO
) VALUES (
	'Rodrigo Paulo de Jimenes Jr.',
	'40413427080',
	'329174769',
	TO_DATE('2021-05-26 12:00:00', 'YYYY-MM-DD HH24:MI:SS'),
	NULL,
	'M',
	45,
	182,
	60
);

INSERT INTO PACIENTE (
	NOME,
	CPF,
	RG,
	DATA_HORA_ENTRADA,
	DATA_HORA_SAIDA,
	SEXO,
	IDADE,
	ALTURA,
	PESO
) VALUES (
	'Demilson Ricardo Carrara Filho',
	'75001571006',
	'498111325',
	TO_DATE('2023-04-01 20:45:32', 'YYYY-MM-DD HH24:MI:SS'),
	NULL,
	'M',
	60,
	174,
	75
);

INSERT INTO PACIENTE (
	NOME,
	CPF,
	RG,
	DATA_HORA_ENTRADA,
	DATA_HORA_SAIDA,
	SEXO,
	IDADE,
	ALTURA,
	PESO
) VALUES (
	'Brenda Galindo de Mendonça',
	'21304986047',
	'145265961',
	TO_DATE('2022-10-01 12:52:40', 'YYYY-MM-DD HH24:MI:SS'),
	NULL,
	'F',
	25,
	149,
	62
);

INSERT INTO PACIENTE (
	NOME,
	CPF,
	RG,
	DATA_HORA_ENTRADA,
	DATA_HORA_SAIDA,
	SEXO,
	IDADE,
	ALTURA,
	PESO
) VALUES (
	'Breno Rogério Carmona Sanches Frias',
	'95293735039',
	'331492313',
	TO_DATE('2022-06-01 08:40:00', 'YYYY-MM-DD HH24:MI:SS'),
	NULL,
	'M',
	35,
	191,
	88
);

INSERT INTO PACIENTE (
	NOME,
	CPF,
	RG,
	DATA_HORA_ENTRADA,
	DATA_HORA_SAIDA,
	SEXO,
	IDADE,
	ALTURA,
	PESO
) VALUES (
	'Cristiane Luiza de Mascarenhas',
	'97708418038',
	'331492313',
	TO_DATE('2021-08-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'),
	NULL,
	'F',
	43,
	172,
	102
);

INSERT INTO PACIENTE (
	NOME,
	CPF,
	RG,
	DATA_HORA_ENTRADA,
	DATA_HORA_SAIDA,
	SEXO,
	IDADE,
	ALTURA,
	PESO
) VALUES (
	'Luana Leonara Mendonça de Holanda',
	'24211065084',
	'217228045',
	TO_DATE('2020-01-01 23:40:00', 'YYYY-MM-DD HH24:MI:SS'),
	NULL,
	'F',
	52,
	180,
	70
);

INSERT INTO PACIENTE (
	NOME,
	CPF,
	RG,
	DATA_HORA_ENTRADA,
	DATA_HORA_SAIDA,
	SEXO,
	IDADE,
	ALTURA,
	PESO
) VALUES (
	'Ana Núbia de Branco',
	'00767832000',
	'206946016',
	TO_DATE('2023-09-04 14:00:00', 'YYYY-MM-DD HH24:MI:SS'),
	NULL,
	'F',
	20,
	160,
	48
);

-- Fonte: https://pt.slideshare.net/rodrigobenfermeiro/fluxograma-manchester
INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Agressão',
	'Agressão refere-se a comportamentos físicos, verbais ou psicológicos que causam dano ou sofrimento a outra pessoa. Pode incluir ataques físicos, ameaças, intimidação ou hostilidade.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Alergia',
	'A alergia é uma resposta imunológica exagerada a substâncias normalmente inofensivas, como pólen, alimentos, picadas de insetos ou medicamentos. Os sintomas podem variar de leves, como coceira e espirros, a graves, incluindo dificuldade respiratória e choque anafilático.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Alteração do Comportamento',
	'Alterações no comportamento referem-se a mudanças significativas na maneira como uma pessoa age ou se relaciona com os outros. Pode incluir agitação, isolamento, agressividade, falta de interesse em atividades comuns, entre outros.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Asma, História de',
	'Uma história de asma indica um histórico médico em que o paciente experimentou problemas respiratórios recorrentes, como sibilância, falta de ar e tosse, associados à obstrução das vias aéreas.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Autoagressão',
	'Autoagressão envolve comportamentos em que uma pessoa causa dano a si mesma deliberadamente. Isso pode incluir cortes, queimaduras, ingestão de substâncias tóxicas, entre outros.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Bebê Chorando',
	'O choro em bebês é uma forma crucial de comunicação. Pode indicar fome, desconforto, sono, fralda suja ou simplesmente a necessidade de atenção. Entender os diferentes tipos de choro pode ajudar os pais a atender às necessidades do bebê.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Cefaleia',
	'Cefaleia refere-se a dores de cabeça. Pode variar de leves a intensas e ser causada por uma variedade de fatores, incluindo tensão, enxaqueca, sinusite ou condições médicas subjacentes.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Convulsões',
	'Convulsões são episódios súbitos e descontrolados de atividade elétrica anormal no cérebro, que podem levar a movimentos involuntários, perda de consciência e outros sintomas. Podem ser causadas por várias condições, incluindo epilepsia, febre alta ou lesões cerebrais.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Corpo Estranho',
	'A presença de um corpo estranho refere-se à entrada acidental de objetos ou substâncias no corpo, muitas vezes causando desconforto, dor ou risco de lesões.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Criança Irritadiça',
	'Uma criança irritadiça demonstra irritação excessiva, mau humor ou desconforto. Pode ser causada por uma variedade de razões, incluindo desconforto físico, fome, cansaço ou necessidade de atenção.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Criança Mancando',
	'Uma criança que está mancando pode estar experimentando dor ou desconforto ao caminhar. Isso pode ser causado por lesões, infecções ou condições médicas subjacentes.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Desmaio no Adulto',
	'O desmaio em adultos refere-se à perda temporária de consciência e pode ser causado por fatores como baixa pressão sanguínea, desidratação, estresse ou condições médicas subjacentes.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Diabetes, História de',
	'Uma história de diabetes indica que o paciente tem um histórico de desequilíbrios nos níveis de açúcar no sangue, o que pode levar a uma variedade de sintomas, incluindo sede excessiva, micção frequente e fadiga.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Diarreia e/ou Vômitos',
	'Diarreia e vômitos são sintomas gastrointestinais que podem ser causados por infecções, intoxicação alimentar, condições médicas ou outros fatores.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Dispnéia em Adulto',
	'A dispneia em adultos refere-se à dificuldade respiratória. Pode ser causada por condições como asma, doença pulmonar obstrutiva crônica (DPOC), insuficiência cardíaca ou outras doenças respiratórias.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Dispnéia em Criança',
	'A dispneia em crianças é caracterizada por dificuldade respiratória. Pode ser causada por infecções respiratórias, alergias, asma ou outros problemas de saúde.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Doença Mental',
	'A doença mental abrange uma variedade de condições que afetam o funcionamento mental e emocional de uma pessoa. Inclui transtornos de ansiedade, depressão, esquizofrenia, entre outros.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Doença Sexualmente Transmissível',
	'Doenças sexualmente transmissíveis (DSTs) são infecções transmitidas por meio de atividades sexuais. Exemplos incluem clamídia, gonorréia, sífilis e HIV.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Dor Abdominal em Adulto',
	'A dor abdominal em adultos pode ser causada por uma variedade de condições, incluindo problemas gastrointestinais, apendicite, pedras nos rins ou outras condições médicas.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Dor Abdominal em Criança',
	'A dor abdominal em crianças pode ser resultado de infecções, problemas gastrointestinais, apendicite ou outras condições. A avaliação médica é importante para determinar a causa.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Dor Cervical',
	'A dor cervical refere-se à dor na região do pescoço. Pode ser causada por lesões, tensão muscular, problemas de coluna ou outras condições.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Dor de Garganta',
	'A dor de garganta pode ser causada por infecções virais ou bacterianas, como resfriados, gripes ou amigdalite. Pode apresentar-se com dificuldade para engolir, vermelhidão e inflamação.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Dor Lombar',
	'A dor lombar é caracterizada por desconforto ou dor na região inferior das costas. Pode ser causada por lesões, má postura, problemas de coluna ou condições médicas subjacentes.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Dor Testicular',
	'A dor testicular pode ser causada por lesões, inflamações, infecções ou torções nos testículos. Avaliação médica é essencial para determinar a causa.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Dor Torácica',
	'A dor torácica pode ser um sintoma de várias condições, incluindo problemas cardíacos, pulmonares ou gastrointestinais. Deve ser avaliada prontamente, especialmente se acompanhada de falta de ar ou dor irradiando para os braços.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Embriaguez Aparente',
	'Indica sinais visíveis de intoxicação alcoólica, como fala arrastada, falta de coordenação motora, mudanças no comportamento e, em casos graves, perda de consciência.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Erupção Cutânea',
	'Refere-se a uma reação na pele que pode apresentar vermelhidão, coceira, inchaço ou descamação. Pode ser causada por alergias, infecções ou condições dermatológicas.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Exposição a Agentes Químicos',
	'Indica contato com substâncias químicas que podem causar irritação, queimaduras ou intoxicação. A avaliação médica é importante para determinar a gravidade e iniciar o tratamento apropriado.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Feridas',
	'Lesões na pele que podem variar em gravidade, desde cortes simples até feridas mais complexas. O tratamento adequado depende da natureza e extensão da ferida.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Gravidez',
	'Refere-se ao estado de uma mulher que está esperando um filho. Os sintomas podem incluir atraso menstrual, náuseas, sensibilidade nos seios e mudanças hormonais.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Hemorragia Digestiva',
	'Sangramento no trato digestivo, que pode se manifestar como sangue nas fezes ou vômito com sangue. Pode ser causado por úlceras, varizes esofágicas ou outras condições gastrointestinais.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Infecções Locais e Abcessos',
	'Indica a presença de infecções localizadas, muitas vezes acompanhadas por inchaço, vermelhidão e dor. Abcessos são acúmulos de pus resultantes de infecções.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Mal Estar em Adulto',
	'Um estado geral de desconforto, podendo ser causado por diversas razões, como infecções, estresse, desidratação ou condições médicas subjacentes.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Mal Estar em Criança',
	'Similar ao mal-estar em adultos, mas considerando as particularidades pediátricas. Pode ser causado por infecções, desconforto físico ou outras condições.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Mordeduras e Picadas',
	'Lesões resultantes de mordidas de animais, insetos ou outros organismos. Podem causar dor, inchaço, vermelhidão e, em alguns casos, transmitir doenças.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Overdose e Envenenamento',
	'Situações em que uma pessoa é exposta a uma quantidade excessiva de substâncias, seja de medicamentos, drogas ou produtos tóxicos. Isso pode levar a sintomas graves e requer atendimento de emergência.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Pais Preocupados',
	'Refere-se a situações em que os pais estão ansiosos ou preocupados com a saúde ou comportamento de seus filhos. Essa preocupação pode ser motivada por sintomas físicos, emocionais ou comportamentais.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Palpitações',
	'Sensação perceptível de batimentos cardíacos irregulares ou acelerados. Pode ser causada por ansiedade, problemas cardíacos ou outras condições médicas.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Problemas Dentários',
	'Inclui condições relacionadas aos dentes e gengivas, como cáries, inflamação gengival, abscessos ou trauma dental.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Problemas em Extremidades',
	'Refere-se a condições que afetam braços, pernas, mãos ou pés. Pode incluir lesões, dor, inchaço ou alterações na sensação.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Problemas em Face',
	'Condições que afetam a região facial, como dor, inchaço, erupções cutâneas ou lesões.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Problemas em Olhos',
	'Inclui condições oculares, como irritação, vermelhidão, coceira, visão embaçada ou outros sintomas relacionados aos olhos.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Problemas em Ouvidos',
	'Condições que afetam os ouvidos, como dor, infecções, perda de audição ou zumbido.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Problemas Urinários',
	'Engloba sintomas relacionados ao sistema urinário, como dificuldade para urinar, dor ao urinar, aumento da frequência urinária ou presença de sangue na urina.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Quedas',
	'Lesões resultantes de cair, podendo variar de contusões leves a fraturas mais graves. Principalmente em idosos, as quedas podem ter sérias consequências.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Queimaduras',
	'Lesões na pele causadas por calor, substâncias químicas ou eletricidade. A gravidade varia de queimaduras leves a graves, exigindo cuidados específicos.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Sangramento Vaginal',
	'Sangramento proveniente da vagina, que pode ser causado por menstruação, gravidez, lesões, infecções ou condições médicas.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Trauma Cranioencefálico',
	'Lesões na cabeça que afetam o cérebro, podendo resultar em concussões, hematomas ou danos mais graves.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Trauma Maior',
	'Lesões graves que afetam múltiplos sistemas do corpo, muitas vezes resultantes de acidentes de trânsito, quedas de altura ou outros eventos traumáticos.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Trauma Toracoabdominal',
	'Lesões que afetam a região do tórax e abdômen, podendo incluir fraturas de costelas, lesões pulmonares ou danos aos órgãos abdominais. Requer avaliação e tratamento urgentes.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Situação de Múltiplas Vitimas — Avaliação Primária',
	'Triagem frente a um acidente com múltiplas vítimas tem um objetivo completamente diferente da classificação de risco usual do dia a dia dos serviços de urgência. Para conseguir este objetivo (que é inicialmente salvar o maior número de pessoas possível e de pois encaminhá-las ao melhor cuidado dentro dos recursos disponíveis), tem sido adotada uma abordagem diferente. Ao invés de se lecionar antes os mais graves, nesta situação são separados os menos graves. Os discriminadores gerais e específicos são substituídos por outros mais simples que fazem uma divisão grosseira dos pacientes em três categorias.'
);

INSERT INTO SINAL (
	NOME,
	DESCRICAO
) VALUES (
	'Situação de Múltiplas Vítimas — Avaliação Secundária',
	'A avaliação secundária é usada para reavaliar os pacientes. O Escore Revisado de Triagem do Trauma — ERTT (Triage Revised Trauma Score —TRTS) é uma abordagem fisiológica mais refinada para classificar grande número de casos. É baseado na pontuação de três parâmetros fisiológicos: estado de consciência, freqüência respiratória e pressão arterial sistólica. Pelo TRTS, as prioridades são alocadas como se segue: 1-10 = Prioridade I, 11 = Prioridade 2, 12 = Prioridade 3, (O = Prioridade 4)'
);

INSERT INTO CLASSIFICACAO (
	DATA_HORA_CLASSIFICACAO,
	GRAVIDADE_ID_GRAVIDADE,
	SINAL_ID_SINAL,
	PACIENTE_ID_PACIENTE,
	AUDITOR_ID_AUDITOR
) VALUES (
	TO_DATE('2021-05-01 10:22:00', 'YYYY-MM-DD HH24:MI:SS'),
	1,
	1,
	1,
	1
);

INSERT INTO CLASSIFICACAO (
	DATA_HORA_CLASSIFICACAO,
	GRAVIDADE_ID_GRAVIDADE,
	SINAL_ID_SINAL,
	PACIENTE_ID_PACIENTE,
	AUDITOR_ID_AUDITOR
) VALUES (
	TO_DATE('2021-05-01 10:23:00', 'YYYY-MM-DD HH24:MI:SS'),
	2,
	2,
	2,
	2
);

INSERT INTO CLASSIFICACAO (
	DATA_HORA_CLASSIFICACAO,
	GRAVIDADE_ID_GRAVIDADE,
	SINAL_ID_SINAL,
	PACIENTE_ID_PACIENTE,
	AUDITOR_ID_AUDITOR
) VALUES (
	TO_DATE('2022-04-12 06:45:10', 'YYYY-MM-DD HH24:MI:SS'),
	3,
	3,
	3,
	3
);

INSERT INTO CLASSIFICACAO (
	DATA_HORA_CLASSIFICACAO,
	GRAVIDADE_ID_GRAVIDADE,
	SINAL_ID_SINAL,
	PACIENTE_ID_PACIENTE,
	AUDITOR_ID_AUDITOR
) VALUES (
	TO_DATE('2021-05-26 12:10:00', 'YYYY-MM-DD HH24:MI:SS'),
	4,
	4,
	4,
	4
);

INSERT INTO CLASSIFICACAO (
	DATA_HORA_CLASSIFICACAO,
	GRAVIDADE_ID_GRAVIDADE,
	SINAL_ID_SINAL,
	PACIENTE_ID_PACIENTE,
	AUDITOR_ID_AUDITOR
) VALUES (
	TO_DATE('2023-04-01 20:50:00', 'YYYY-MM-DD HH24:MI:SS'),
	5,
	5,
	5,
	5
);

INSERT INTO CLASSIFICACAO (
	DATA_HORA_CLASSIFICACAO,
	GRAVIDADE_ID_GRAVIDADE,
	SINAL_ID_SINAL,
	PACIENTE_ID_PACIENTE,
	AUDITOR_ID_AUDITOR
) VALUES (
	TO_DATE('2022-10-01 12:55:00', 'YYYY-MM-DD HH24:MI:SS'),
	1,
	6,
	6,
	6
);

INSERT INTO CLASSIFICACAO (
	DATA_HORA_CLASSIFICACAO,
	GRAVIDADE_ID_GRAVIDADE,
	SINAL_ID_SINAL,
	PACIENTE_ID_PACIENTE,
	AUDITOR_ID_AUDITOR
) VALUES (
	TO_DATE('2022-06-01 08:45:00', 'YYYY-MM-DD HH24:MI:SS'),
	2,
	7,
	7,
	7
);

INSERT INTO CLASSIFICACAO (
	DATA_HORA_CLASSIFICACAO,
	GRAVIDADE_ID_GRAVIDADE,
	SINAL_ID_SINAL,
	PACIENTE_ID_PACIENTE,
	AUDITOR_ID_AUDITOR
) VALUES (
	TO_DATE('2021-08-01 12:05:00', 'YYYY-MM-DD HH24:MI:SS'),
	3,
	8,
	8,
	8
);

INSERT INTO CLASSIFICACAO (
	DATA_HORA_CLASSIFICACAO,
	GRAVIDADE_ID_GRAVIDADE,
	SINAL_ID_SINAL,
	PACIENTE_ID_PACIENTE,
	AUDITOR_ID_AUDITOR
) VALUES (
	TO_DATE('2020-01-01 23:45:00', 'YYYY-MM-DD HH24:MI:SS'),
	4,
	9,
	9,
	9
);

INSERT INTO CLASSIFICACAO (
	DATA_HORA_CLASSIFICACAO,
	GRAVIDADE_ID_GRAVIDADE,
	SINAL_ID_SINAL,
	PACIENTE_ID_PACIENTE,
	AUDITOR_ID_AUDITOR
) VALUES (
	TO_DATE('2023-09-04 14:05:00', 'YYYY-MM-DD HH24:MI:SS'),
	5,
	10,
	10,
	10
);

-- 1. Uma consulta simples envolvendo SELECT/FROM/WHERE/ORDER BY.
-- Retorna todos os pacientes do sexo masculino ordenados pelo nome de forma decrescente
SELECT
	*
FROM
	PACIENTE
WHERE
	SEXO = 'M'
ORDER BY
	NOME DESC;

-- 2. Uma consulta envolvendo uma ou mais junções de tabela, contendo: SELECT/FROM/WHERE/ORDER BY
-- Retorna o nome e o nível de gravidade dos pacientes que estão na emergência
SELECT
	P.NOME,
	G.NOME_GRAVIDADE AS "NIVEL DE GRAVIDADE"
FROM
	PACIENTE      P
	INNER JOIN CLASSIFICACAO C
	ON P.ID_PACIENTE = C.PACIENTE_ID_PACIENTE
	INNER JOIN GRAVIDADE G
	ON C.GRAVIDADE_ID_GRAVIDADE = G.ID_GRAVIDADE
WHERE
	G.NOME_GRAVIDADE = 'EMERGÊNCIA';

-- 3. Uma consulta envolvendo função de grupo e agrupamento
-- Retorna a quantidade de classificações por nível de gravidade
SELECT
	COUNT(*),
	G.NOME_GRAVIDADE AS "NIVEL DE GRAVIDADE"
FROM
	CLASSIFICACAO C
	INNER JOIN GRAVIDADE G
	ON C.GRAVIDADE_ID_GRAVIDADE = G.ID_GRAVIDADE
GROUP BY
	G.NOME_GRAVIDADE;

-- 4. Uma consulta envolvendo função de grupo, agrupamento com filtro (HAVING) e junção de tabelas
-- Retorna a quantidade de classificações por nível de gravidade, onde o nível de gravidade é diferente de EMERGÊNCIA
SELECT
	COUNT(*),
	G.NOME_GRAVIDADE AS "NIVEL DE GRAVIDADE"
FROM
	CLASSIFICACAO C
	INNER JOIN GRAVIDADE G
	ON C.GRAVIDADE_ID_GRAVIDADE = G.ID_GRAVIDADE
GROUP BY
	G.NOME_GRAVIDADE
HAVING
	G.NOME_GRAVIDADE <> 'EMERGÊNCIA';