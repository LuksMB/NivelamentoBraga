USE operacoes_medicas;

-- Contar registros
SELECT COUNT(*) FROM transacoes;

-- Visualizar alguns registros
SELECT * FROM transacoes LIMIT 10;

-- Verificar valores distintos
SELECT DISTINCT reg_ans FROM transacoes;

-- Verifica se existem registros com a data exata do último trimestre
SELECT COUNT(*) 
FROM transacoes 
WHERE data = '2024-10-01';

-- Verifica se existem registros para o ano de 2024
SELECT COUNT(*) 
FROM transacoes 
WHERE data BETWEEN '2024-01-01' AND '2024-12-31';

-- Verifique se existem registros com a descrição da categoria específica
SELECT COUNT(*) 
FROM transacoes 
WHERE descricao LIKE 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR ';