SELECT 
    reg_ans AS Operadora,
    ROUND(SUM(vl_saldo_final), 2) AS Total_Despesas_Anual,
    COUNT(*) AS Quantidade_Registros
FROM 
    transacoes
WHERE 
    data BETWEEN '2024-01-01' AND '2024-12-31'
    AND descricao LIKE 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
GROUP BY 
    reg_ans
ORDER BY 
    Total_Despesas_Anual DESC
LIMIT 10;