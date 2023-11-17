CREATE TABLE AUDITOR (
    ID_AUDITOR INTEGER NOT NULL,
    NOME VARCHAR2(50 CHAR) NOT NULL,
    CPF VARCHAR2(11 CHAR) NOT NULL,
    CRM VARCHAR2(20 CHAR),
    COREN VARCHAR2(20 CHAR),
    ESPECIALIDADE VARCHAR2(50 CHAR)
);

ALTER TABLE AUDITOR ADD CONSTRAINT AUDITOR_PK PRIMARY KEY ( ID_AUDITOR );

CREATE TABLE CLASSIFICACAO (
    ID_CLASSIFICACAO INTEGER NOT NULL,
    DATA_HORA_CLASSIFICACAO DATE NOT NULL,
    GRAVIDADE_ID_GRAVIDADE INTEGER NOT NULL,
    SINAL_ID_SINAL INTEGER NOT NULL,
    PACIENTE_ID_PACIENTE INTEGER NOT NULL,
    AUDITOR_ID_AUDITOR INTEGER NOT NULL
);


ALTER TABLE CLASSIFICACAO ADD CONSTRAINT CLASSIFICACAO_RISCO_PK PRIMARY KEY ( ID_CLASSIFICACAO );

CREATE TABLE GRAVIDADE (
    ID_GRAVIDADE INTEGER NOT NULL,
    NOME_GRAVIDADE VARCHAR2(20 CHAR) NOT NULL,
    NOME_COR VARCHAR2(20 CHAR) NOT NULL,
    HEXADECIMAL_COR VARCHAR2(6 CHAR)
);

ALTER TABLE GRAVIDADE ADD CONSTRAINT GRAVIDADE_PK PRIMARY KEY ( ID_GRAVIDADE );

CREATE TABLE PACIENTE (
    ID_PACIENTE INTEGER NOT NULL,
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
    ID_SINAL INTEGER NOT NULL,
    NOME VARCHAR2(60 CHAR) NOT NULL,
    DESCRICAO VARCHAR2(700 CHAR)
);

ALTER TABLE SINAL ADD CONSTRAINT SINAL_APRESENTADO_PK PRIMARY KEY ( ID_SINAL );

ALTER TABLE CLASSIFICACAO ADD CONSTRAINT CLASSIFICACAO_AUDITOR_FK FOREIGN KEY ( AUDITOR_ID_AUDITOR ) REFERENCES AUDITOR ( ID_AUDITOR );

ALTER TABLE CLASSIFICACAO ADD CONSTRAINT CLASSIFICACAO_GRAVIDADE_FK FOREIGN KEY ( GRAVIDADE_ID_GRAVIDADE ) REFERENCES GRAVIDADE ( ID_GRAVIDADE );

ALTER TABLE CLASSIFICACAO ADD CONSTRAINT CLASSIFICACAO_PACIENTE_FK FOREIGN KEY ( PACIENTE_ID_PACIENTE ) REFERENCES PACIENTE ( ID_PACIENTE) ;

ALTER TABLE CLASSIFICACAO ADD CONSTRAINT CLASSIFICACAO_SINAL_FK FOREIGN KEY ( SINAL_ID_SINAL ) REFERENCES SINAL ( ID_SINAL );
