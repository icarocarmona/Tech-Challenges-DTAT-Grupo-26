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
END AS RESTRINGIU_CONTATO
FROM
  `basedosdados.br_ibge_pnad_covid.microdados`
LIMIT
  1000;
