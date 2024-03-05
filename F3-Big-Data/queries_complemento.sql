SELECT
  sigla_uf AS UF,
  capital,
  a002 AS IDADE,
  CASE
    WHEN CAST(a003 AS int64) = 1 THEN 'Homem'
  ELSE
  'Mulher'
END
  AS SEXO,
  CASE
    WHEN CAST(a004 AS int64) = 1 THEN 'Branca'
    WHEN CAST(a004 AS int64) = 2 THEN 'Preta'
    WHEN CAST(a004 AS int64) = 3 THEN 'Amarela'
    WHEN CAST(a004 AS int64) = 4 THEN 'Parda'
    WHEN CAST(a004 AS int64) = 5 THEN 'Indígena'
END
  AS COR_RACA,
  CASE
    WHEN CAST(b0011 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(b0011 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS Febre,
  CASE
    WHEN CAST(b0012 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(b0012 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  Tosse,
  CASE
    WHEN CAST(b0013 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(b0013 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS Dor_de_garganta,
  CASE
    WHEN CAST(b0014 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(b0014 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS Dificuldade_para_respirar,
  CASE
    WHEN CAST(b0015 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(b0015 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS Dor_de_cabeca,
  CASE
    WHEN CAST(b0016 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(b0016 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS Dor_no_peito,
  CASE
    WHEN CAST(b0017 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(b0017 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS Nausea_enjoo,
  CASE
    WHEN CAST(b0018 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(b0018 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  Nariz_entupido_ou_escorrendo,
  CASE
    WHEN CAST(b0019 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(b0019 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS Fadiga_cansaco,
  CASE
    WHEN CAST(b00110 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(b00110 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS Dor_nos_olhos,
  CASE
    WHEN CAST(b00111 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(b00111 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS Perda_cheiro_ou_sabor,
  CASE
    WHEN CAST(b00112 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(b00112 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS Dor_muscular_dor_corpo,
  CASE
    WHEN CAST(b00113 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(b00113 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS Diarreia,
  CASE
    WHEN CAST(B002 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(B002 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS FOI_ESTABELECIMENTO_SAUDE,
  CASE
    WHEN CAST(B0041 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(B0041 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS ATEND_PS_UBS_ESF,
  CASE
    WHEN CAST(B0042 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(B0042 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS ATEND_PS_SUS_UPA,
  CASE
    WHEN CAST(B0043 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(B0043 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS ATEND_HOSP_SUS,
  CASE
    WHEN CAST(B0044 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(B0044 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS ATEND_AMBU_CONSPRI_FA,
  CASE
    WHEN CAST(B0045 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(B0045 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS ATEND_PS_FA,
  CASE
    WHEN CAST(B0046 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(B0046 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS ATEND_HOSP_PRIV_FA,
  CASE
    WHEN CAST(B005 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(B005 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS INTERNADO_UM_DIA_OU_MAIS,
  CASE
    WHEN CAST(B007 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(B007 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS PLANO_SAUDE,
  CASE
    WHEN CAST(B008 AS INT64) = 1 THEN 'Sim'
    WHEN CAST(B008 AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS FEZ_TESTE,
CASE
    WHEN CAST(B009A AS INT64) = 1 THEN 'Sim'
    WHEN CAST(B009A AS INT64) = 2 THEN 'Não'
  ELSE
  'Ignorado'
END
  AS EXAME_COTONETE_SWAB,
CASE 
	WHEN CAST(B0101 AS INT64) = 1 THEN 'Sim'
	WHEN CAST(B0101 AS INT64) = 2 THEN 'Não'
	ELSE 'Ignorado'
END AS DIAG_DIABETES,
CASE 
	WHEN CAST(B0102 AS INT64) = 1 THEN 'Sim'
	WHEN CAST(B0102 AS INT64) = 2 THEN 'Não'
	ELSE 'Ignorado'
END AS DIAG_HIPERTENSAO,
CASE 
	WHEN CAST(B0103 AS INT64) = 1 THEN 'Sim'
	WHEN CAST(B0103 AS INT64) = 2 THEN 'Não'
	ELSE 'Ignorado'
END AS DIAG_ASMA,
CASE 
	WHEN CAST(B0104 AS INT64) = 1 THEN 'Sim'
	WHEN CAST(B0104 AS INT64) = 2 THEN 'Não'
	ELSE 'Ignorado'
END AS DIAG_DOEN_CORACAO,
CASE 
	WHEN CAST(B0105 AS INT64) = 1 THEN 'Sim'
	WHEN CAST(B0105 AS INT64) = 2 THEN 'Não'
	ELSE 'Ignorado'
END AS DIAG_DEPRESSAO,
CASE 
	WHEN CAST(B0106 AS INT64) = 1 THEN 'Sim'
	WHEN CAST(B0106 AS INT64) = 2 THEN 'Não'
	ELSE 'Ignorado'
END AS DIAG_CANCER,
CASE 
	WHEN CAST(B0106 AS INT64) = 1 THEN 'Não fez restrição, levou vida normal como antes da pandemia'
	WHEN CAST(B0106 AS INT64) = 2 THEN 'Reduziu o contato com as pessoas, mas continuou saindo de casa para trabalho ou atividades não essenciais e/ou recebendo visitas'
	WHEN CAST(B0106 AS INT64) = 3 THEN 'Ficou em casa e só saiu em caso de necessidade básica (comprar comida, remédio, ir ao médico etc.)'
	WHEN CAST(B0106 AS INT64) = 4 THEN 'Ficou rigorosamente isolado em casa'
	ELSE 'Ignorado'
END AS RESTRINGIU_CONTATO,
CASE 
      WHEN CAST(B0041 AS INT64) = 1 THEN 'Sim'
      WHEN CAST(B0041 AS INT64) = 2 THEN 'Não'
      ELSE 'Ignorado'
END AS BUSC_ATEND_POSTO,
 CASE 
      WHEN CAST(B0042 AS INT64) = 1 THEN 'Sim'
      WHEN CAST(B0042 AS INT64) = 2 THEN 'Não'
      ELSE 'Ignorado'
END AS BUSC_ATEND_PSOCORRO,     
CASE 
      WHEN CAST(B0043 AS INT64) = 1 THEN 'Sim'
      WHEN CAST(B0043 AS INT64) = 2 THEN 'Não'
      ELSE 'Ignorado'
END AS BUSC_ATEND_HOPITAL,
CASE 
      WHEN CAST(B0044 AS INT64) = 1 THEN 'Sim'
      WHEN CAST(B0044 AS INT64) = 2 THEN 'Não'
      ELSE 'Ignorado'
END AS BUSC_ATEND_AMB,
CASE 
      WHEN CAST(B0045 AS INT64) = 1 THEN 'Sim'
      WHEN CAST(B0045 AS INT64) = 2 THEN 'Não'
      ELSE 'Ignorado'
END AS BUSC_ATEND_HOSP_PRIVADO,
CASE 
      WHEN CAST(C001 AS INT64) = 1 THEN 'Sim'
      WHEN CAST(C001 AS INT64) = 2 THEN 'Não'
      ELSE 'Ignorado'
END AS TRAB_SEM_PASSADA,
CASE 
      WHEN CAST(C002 AS INT64) = 1 THEN 'Sim'
      WHEN CAST(C002 AS INT64) = 2 THEN 'Não'
      ELSE 'Ignorado'
END AS AFAST_TRAB_SEM_PASSADA,
CASE 
      WHEN CAST(C003 AS INT64) = 1 THEN 'Isolamento'
      WHEN CAST(C003 AS INT64) = 2 THEN 'Féras ou folga'
      WHEN CAST(C003 AS INT64) = 3 THEN 'Licença maternidade'
      WHEN CAST(C003 AS INT64) = 4 THEN 'Licença remunerada por motivo de saúde'
      WHEN CAST(C003 AS INT64) = 5 THEN 'Outro tipo de licença remunerada'
      WHEN CAST(C003 AS INT64) = 6 THEN 'Afastamento do próprio negócio'
      WHEN CAST(C003 AS INT64) = 7 THEN 'Fatores ocasionais ('
      WHEN CAST(C003 AS INT64) = 8 THEN 'Outro motivo'
      ELSE 'Ignorado'
END AS MOT_AFASTAMENTO,
CASE 
      WHEN CAST(C007 AS INT64) = 1 THEN 'Trabalhador doméstico'
      WHEN CAST(C007 AS INT64) = 2 THEN 'Militar do exército'
      WHEN CAST(C007 AS INT64) = 3 THEN 'Policial militar ou bombeiro militar'
      WHEN CAST(C007 AS INT64) = 4 THEN 'Empregado do setor privado'
      WHEN CAST(C007 AS INT64) = 5 THEN 'Outro tipo de licença remunerada'
      WHEN CAST(C007 AS INT64) = 6 THEN 'Empregador'
      WHEN CAST(C007 AS INT64) = 7 THEN 'Conta própria'
      WHEN CAST(C007 AS INT64) = 8 THEN 'Trabalhador não remunerado'
      WHEN CAST(C007 AS INT64) = 9 THEN 'Estava fora do mercado de trabalho'
      ELSE 'Ignorado'
END AS TIPO_TRABALHO,
CASE 
      WHEN CAST(C007C AS INT64) = 1 THEN 'Empregado doméstico(em domicílios particulares)'
      WHEN CAST(C007C AS INT64) = 2 THEN 'Faxineiro (em empresa pública ou privada)'
      WHEN CAST(C007C AS INT64) = 3 THEN 'Auxiliar de escritório'
      WHEN CAST(C007C AS INT64) = 4 THEN 'Secretária, recepcionista'
      WHEN CAST(C007C AS INT64) = 5 THEN 'Operador de Telemarketing'
      WHEN CAST(C007C AS INT64) = 6 THEN 'Comerciante'
      WHEN CAST(C007C AS INT64) = 7 THEN 'Balconista, vendedor de loja'
      WHEN CAST(C007C AS INT64) = 8 THEN 'Vendedor a domicílio'
      WHEN CAST(C007C AS INT64) = 9 THEN 'Vendedor ambulante'
      WHEN CAST(C007C AS INT64) = 10 THEN 'Cozinheiro e garçom'
      WHEN CAST(C007C AS INT64) = 11 THEN 'Padeiro, açougueiro e doceiro'
      WHEN CAST(C007C AS INT64) = 12 THEN 'Agricultor, criador de animais'
      WHEN CAST(C007C AS INT64) = 13 THEN 'Auxiliar da agropecuária'
      WHEN CAST(C007C AS INT64) = 14 THEN 'Motorista de aplicativo'
      WHEN CAST(C007C AS INT64) = 15 THEN 'Caminhoneiro'
      WHEN CAST(C007C AS INT64) = 16 THEN 'Motoboy'
      WHEN CAST(C007C AS INT64) = 17 THEN 'Entregador de mercadorias'
      WHEN CAST(C007C AS INT64) = 18 THEN 'Pedreiro, servente de pedreiro'
      WHEN CAST(C007C AS INT64) = 19 THEN 'Mecânico de veículos, máquinas industriais'
      WHEN CAST(C007C AS INT64) = 20 THEN 'Artesão, costureiro e sapateiro'
      WHEN CAST(C007C AS INT64) = 21 THEN 'Cabeleireiro, manicure e afins'
      WHEN CAST(C007C AS INT64) = 22 THEN 'Operador de máquinas, montador na indústria'
      WHEN CAST(C007C AS INT64) = 23 THEN 'Auxiliar de produção, de carga e descarga'
      WHEN CAST(C007C AS INT64) = 24 THEN 'Professor da educação infantil'
      WHEN CAST(C007C AS INT64) = 25 THEN 'Pedagogo, professor de idiomas, música, arte e reforço escolar'
      WHEN CAST(C007C AS INT64) = 26 THEN 'Médico, enfermeiro, profissionais de saúde de nível superior'
      WHEN CAST(C007C AS INT64) = 27 THEN 'Técnico, profissional da saúde de nível médio'
      WHEN CAST(C007C AS INT64) = 28 THEN 'Cuidador de crianças, doentes ou idosos'
      WHEN CAST(C007C AS INT64) = 29 THEN 'Segurança, vigilante, outro trabalhador dos serviços de proteção'
      WHEN CAST(C007C AS INT64) = 30 THEN 'Policial civil'
      WHEN CAST(C007C AS INT64) = 31 THEN 'Porteiro, zelador'
      WHEN CAST(C007C AS INT64) = 32 THEN 'Artista, religioso (padre, pastor etc.)'
      WHEN CAST(C007C AS INT64) = 33 THEN 'Diretor, gerente, cargo político ou comissionado'
      WHEN CAST(C007C AS INT64) = 34 THEN 'Outra profissão de nível superior (advogado, engenheiro, contador, jornalista etc.)'
      WHEN CAST(C007C AS INT64) = 35 THEN 'Outro técnico ou profissional de nível médio'
      WHEN CAST(C007C AS INT64) = 36 THEN 'Outros'      
      ELSE 'Ignorado'
END AS TIPO_TRABALHO,
CASE 
      WHEN CAST(C007D AS INT64) = 1 THEN 'Agricultura, pecuária'
      WHEN CAST(C007D AS INT64) = 2 THEN 'Extração de petróleo, carvão mineral'
      WHEN CAST(C007D AS INT64) = 3 THEN 'Indústria da transformação'
      WHEN CAST(C007D AS INT64) = 4 THEN 'Fornecimento de eletricidade e gás'
      WHEN CAST(C007D AS INT64) = 5 THEN 'Construção'
      WHEN CAST(C007D AS INT64) = 6 THEN 'Comércio no atacado e varejo'
      WHEN CAST(C007D AS INT64) = 7 THEN 'Balconista, vendedor de loja'
      WHEN CAST(C007D AS INT64) = 8 THEN 'Transporte de passageiros'
      WHEN CAST(C007D AS INT64) = 9 THEN 'Transporte de mercadorias'
      WHEN CAST(C007D AS INT64) = 10 THEN 'Correios, serviços de entregas'
      WHEN CAST(C007D AS INT64) = 11 THEN 'Hospedagem (hotéis, pousadas etc.)'
      WHEN CAST(C007D AS INT64) = 12 THEN 'Serviço de alimentação'
      WHEN CAST(C007D AS INT64) = 13 THEN 'Informação e comunicação (jornais, rádio)'
      WHEN CAST(C007D AS INT64) = 14 THEN 'Bancos, atividades financeiras e de seguros'
      WHEN CAST(C007D AS INT64) = 15 THEN 'Atividades imobiliárias'
      WHEN CAST(C007D AS INT64) = 16 THEN 'Escritórios de advocacia, engenharia, publicidade'
      WHEN CAST(C007D AS INT64) = 17 THEN 'Atividades de locação de mão de obra'
      WHEN CAST(C007D AS INT64) = 18 THEN 'Administração pública'
      WHEN CAST(C007D AS INT64) = 19 THEN 'Educação'
      WHEN CAST(C007D AS INT64) = 20 THEN 'Saúde humana e assistência social'
      WHEN CAST(C007D AS INT64) = 21 THEN 'Organizações religiosas, sindicatos e associações'
      WHEN CAST(C007D AS INT64) = 22 THEN 'Atividade artísticas, esportivas e de recreação'
      WHEN CAST(C007D AS INT64) = 23 THEN 'Cabeleireiros, tratamento de beleza e serviços pessoais '
      WHEN CAST(C007D AS INT64) = 24 THEN 'Serviço doméstico remunerado '
      WHEN CAST(C007D AS INT64) = 25 THEN 'Outro'
      ELSE 'Ignorado'
END AS PRINc_ATIV_EMPRESA,
CASE 
      WHEN CAST(C011A AS INT64) = 1 THEN 'Valor em dinheiro'
      WHEN CAST(C011A AS INT64) = 2 THEN 'Valor em mercadoria'
      ELSE 'Ignorado'
END AS QUANTO_RECEBEU,
FROM
  basedosdados.br_ibge_pnad_covid.microdados 
  WHERE B0106 != 'Ignorado'
LIMIT
  1000;
