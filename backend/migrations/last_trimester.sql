SELECT 
    reg_ans AS Operadora,
    ROUND(SUM(vl_saldo_final), 2) AS Total_Despesas
FROM 
    transacoes
WHERE 
    data = '2024-10-01'
    AND descricao LIKE 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
GROUP BY 
    reg_ans
ORDER BY 
    Total_Despesas DESC
LIMIT 10;