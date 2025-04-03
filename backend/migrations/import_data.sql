USE operacoes_medicas;

--  TROCAR PELO CAMINHO BRUTO DO ARQUIVO NO SEU SISTEMA OU COLOCAR O ARQUIVO NA PASTA DO SQL
LOAD DATA INFILE 'caminho/ate/os/dados_consolidados.csv' INTO
TABLE transacoes FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS (
    @data,
    reg_ans,
    cd_conta_contabil,
    descricao,
    vl_saldo_inicial,
    vl_saldo_final
)
SET
    data = CASE
        WHEN @data = '01/10/2023' THEN '2023-10-01'
        ELSE @data
    END;