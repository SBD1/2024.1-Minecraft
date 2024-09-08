-- Tabela Instância Estrutura
DO
$$
DECLARE
    chunk_rec RECORD;
    rand_num FLOAT;
    estrutura_existente INTEGER;
    nova_estrutura_id INTEGER;
BEGIN
    -- Iterando por todos os chunks em todos os mapas
    FOR chunk_rec IN 
        SELECT numero, nome_bioma, nome_mapa 
        FROM Chunk
    LOOP
        -- Verifica se o chunk já possui uma estrutura
        SELECT COUNT(*) INTO estrutura_existente
        FROM InstanciaEstrutura
        WHERE numero_chunk = chunk_rec.numero
        AND nome_mapa = chunk_rec.nome_mapa;

        -- Se já houver uma estrutura, pula para o próximo chunk
        IF estrutura_existente > 0 THEN
            CONTINUE;
        END IF;

        -- Superfície
        IF chunk_rec.nome_mapa = 'Superfície' THEN
            -- Templo da Selva
            IF chunk_rec.nome_bioma = 'Selva' THEN
                rand_num := random() * 100;
                IF rand_num <= 5.00 THEN
                    -- Chamar stored procedure para inserir a estrutura
                    CALL inserir_inst_estrutura('Templo da Selva', chunk_rec.nome_bioma, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);

                    -- Chamar stored procedure para inserir mobs na estrutura
                    CALL inserir_inst_mob('zumbi', 25, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);
                    CALL inserir_inst_mob('esqueleto', 20, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);
                    
                    CONTINUE;
                END IF;
            END IF;

            -- Templo do Deserto
            IF chunk_rec.nome_bioma = 'Deserto' THEN
                rand_num := random() * 100;
                IF rand_num <= 5.00 THEN
                    -- Chamar stored procedure para inserir a estrutura
                    CALL inserir_inst_estrutura('Templo do Deserto', chunk_rec.nome_bioma, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);

                    -- Chamar stored procedure para inserir mobs na estrutura
                    CALL inserir_inst_mob('zumbi', 25, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);
                    CALL inserir_inst_mob('zumbi', 25, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);

                    CONTINUE;
                END IF;
            END IF;

            -- Cabana da bruxa
            IF chunk_rec.nome_bioma = 'Pântano' THEN
                rand_num := random() * 100;
                IF rand_num <= 7.00 THEN
                    -- Chamar stored procedure para inserir a estrutura
                    CALL inserir_inst_estrutura('Cabana da bruxa', chunk_rec.nome_bioma, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);

                    -- Chamar stored procedure para inserir mob na Cabana da bruxa
                    CALL inserir_inst_mob('bruxa', 26, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);

                    CONTINUE;
                END IF;
            END IF;

            -- Portal em Ruínas
            IF chunk_rec.nome_bioma IN ('Deserto', 'Planície', 'Floresta', 'Selva', 'Pântano', 'Montanha', 'Neve') THEN
                rand_num := random() * 100;
                IF rand_num <= 10.00 THEN
                    -- Chamar stored procedure para inserir a estrutura
                    CALL inserir_inst_estrutura('Portal em Ruínas', chunk_rec.nome_bioma, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);

                    -- Chamar stored procedure para inserir mob no Portal em Ruínas
                    CALL inserir_inst_mob('piglin', 16, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);
                    CALL inserir_inst_mob('piglin zumbi', 20, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);

                    CONTINUE;
                END IF;
            END IF;

            -- Vila
            IF chunk_rec.nome_bioma IN ('Deserto', 'Planície', 'Floresta', 'Montanha', 'Neve') THEN
                rand_num := random() * 100;
                IF rand_num <= 20.00 THEN
                    -- Chamar stored procedure para inserir a estrutura
                    CALL inserir_inst_estrutura('Vila', chunk_rec.nome_bioma, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);

                    -- Chamar stored procedure para inserir NPCs na Vila
                    CALL inserir_inst_mob('aldeão', 20, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);
                    CALL inserir_inst_mob('aldeão', 20, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);
                    CALL inserir_inst_mob('golem de ferro', 100, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);

                    CONTINUE;
                END IF;
            END IF;

            -- Posto Avançado
            IF chunk_rec.nome_bioma IN ('Planície', 'Deserto', 'Montanha') THEN
                rand_num := random() * 100;
                IF rand_num <= 8.00 THEN
                    -- Chamar stored procedure para inserir a estrutura
                    CALL inserir_inst_estrutura('Posto Avançado', chunk_rec.nome_bioma, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);

                    -- Chamar stored procedure para inserir mobs no Posto Avançado
                    CALL inserir_inst_mob('pilhador', 24, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);
                    CALL inserir_inst_mob('pilhador', 24, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);

                    CONTINUE;
                END IF;
            END IF;
        END IF;

        -- Cavernas
        IF chunk_rec.nome_mapa = 'Cavernas' THEN
            -- Fortaleza do Fim
            IF chunk_rec.nome_bioma = 'Fortaleza' THEN
                rand_num := random() * 100;
                IF rand_num <= 5.00 THEN
                    -- Chamar stored procedure para inserir a estrutura
                    CALL inserir_inst_estrutura('Fortaleza do Fim', chunk_rec.nome_bioma, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);

                    -- Chamar stored procedure para inserir mobs na Fortaleza do Fim
                    CALL inserir_inst_mob('esqueleto', 20, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);
                    CALL inserir_inst_mob('blaze', 20, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);

                    CONTINUE;
                END IF;
            END IF;

            -- Mina Abandonada
            IF chunk_rec.nome_bioma = 'Caverna' THEN
                rand_num := random() * 100;
                IF rand_num <= 10.00 THEN
                    -- Chamar stored procedure para inserir a estrutura
                    CALL inserir_inst_estrutura('Mina Abandonada', chunk_rec.nome_bioma, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);

                    -- Chamar stored procedure para inserir mobs na Mina Abandonada
                    CALL inserir_inst_mob('aranha', 16, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);

                    CONTINUE;
                END IF;
            END IF;
        END IF;

        -- Nether
        IF chunk_rec.nome_mapa = 'Nether' THEN
            -- Bastião em Ruínas
            IF chunk_rec.nome_bioma = 'Descampado' THEN
                rand_num := random() * 100;
                IF rand_num <= 3.00 THEN
                    -- Chamar stored procedure para inserir a estrutura
                    CALL inserir_inst_estrutura('Bastião em Ruínas', chunk_rec.nome_bioma, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);

                    -- Chamar stored procedure para inserir mobs no Bastião em Ruínas
                    CALL inserir_inst_mob('piglin', 20, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);
                    CALL inserir_inst_mob('piglin zumbi', 20, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);
                    CALL inserir_inst_mob('esqueleto wither', 20, chunk_rec.numero, chunk_rec.nome_mapa, nova_estrutura_id);

                    CONTINUE;
                END IF;
            END IF;
        END IF;
        
    END LOOP;
END
$$;

-- Tabela Instância Mob
DO
$$
DECLARE
    chunk_rec RECORD;
    rand_num FLOAT;
BEGIN
    -- Iterando por todos os chunks na tabela Chunk
    FOR chunk_rec IN 
        SELECT numero, nome_bioma, nome_mapa 
        FROM Chunk
    LOOP
        -- Superfície
        IF chunk_rec.nome_mapa = 'Superfície' THEN
            -- galinha (spawn em Planície, Floresta)
            IF chunk_rec.nome_bioma IN ('Planície', 'Floresta') THEN
                rand_num := random() * 100;
                IF rand_num <= 45.00 THEN
                    CALL inserir_inst_mob('galinha', 5, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;
            END IF;

            -- vaca e porco (spawn em Planície)
            IF chunk_rec.nome_bioma = 'Planície' THEN
                rand_num := random() * 100;
                IF rand_num <= 45.00 THEN
                    CALL inserir_inst_mob('vaca', 10, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;

                rand_num := random() * 100;
                IF rand_num <= 35.00 THEN
                    CALL inserir_inst_mob('porco', 10, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;
            END IF;

            -- ovelha (spawn em Planície, Montanha)
            IF chunk_rec.nome_bioma IN ('Planície', 'Montanha') THEN
                rand_num := random() * 100;
                IF rand_num <= 30.00 THEN
                    CALL inserir_inst_mob('ovelha', 8, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;
            END IF;

            -- peixe, golfinho e guardião (spawn em Lago)
            IF chunk_rec.nome_bioma = 'Lago' THEN
                rand_num := random() * 100;
                IF rand_num <= 30.00 THEN
                    CALL inserir_inst_mob('peixe', 3, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;

                rand_num := random() * 100;
                IF rand_num <= 10.00 THEN
                    CALL inserir_inst_mob('golfinho', 10, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;

                rand_num := random() * 100;
                IF rand_num <= 5.00 THEN
                    CALL inserir_inst_mob('guardião', 30, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;
            END IF;

            -- urso polar e golem de neve (spawn em Neve)
            IF chunk_rec.nome_bioma = 'Neve' THEN
                rand_num := random() * 100;
                IF rand_num <= 25.00 THEN
                    CALL inserir_inst_mob('urso polar', 30, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;

                rand_num := random() * 100;
                IF rand_num <= 15.00 THEN
                    CALL inserir_inst_mob('golem de neve', 4, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;
            END IF;
        END IF;

        -- Cavernas
        IF chunk_rec.nome_mapa = 'Cavernas' THEN
            -- Mobs hostis (spawn em Caverna)
            IF chunk_rec.nome_bioma IN ('Caverna', 'Fortaleza') THEN
                rand_num := random() * 100;
                IF rand_num <= 40.00 THEN
                    CALL inserir_inst_mob('esqueleto', 20, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;

                rand_num := random() * 100;
                IF rand_num <= 40.00 THEN
                    CALL inserir_inst_mob('creeper', 20, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;

                rand_num := random() * 100;
                IF rand_num <= 50.00 THEN
                    CALL inserir_inst_mob('zumbi', 25, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;

                rand_num := random() * 100;
                IF rand_num <= 30.00 THEN
                    CALL inserir_inst_mob('aranha', 16, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;

                rand_num := random() * 100;
                IF rand_num <= 20.00 THEN
                    CALL inserir_inst_mob('enderman', 26, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;

                rand_num := random() * 100;
                IF rand_num <= 10.00 THEN
                    CALL inserir_inst_mob('bruxa', 26, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;
            END IF;

            -- warden (spawn em Cidade ancestral)
            IF chunk_rec.nome_bioma = 'Cidade ancestral' THEN
                rand_num := random() * 100;
                IF rand_num <= 5.00 THEN
                    CALL inserir_inst_mob('warden', 500, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;
            END IF;
        END IF;

        -- Nether
        IF chunk_rec.nome_mapa = 'Nether' THEN
            -- piglin e hoglin (spawn em Floresta carmesim)
            IF chunk_rec.nome_bioma = 'Floresta carmesim' THEN
                rand_num := random() * 100;
                IF rand_num <= 45.00 THEN
                    CALL inserir_inst_mob('piglin', 16, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;
                IF rand_num <= 40.00 THEN
                    CALL inserir_inst_mob('hoglin', 40, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;
            END IF;

            -- ghast e piglin zumbi (spawn em Descampado)
            IF chunk_rec.nome_bioma = 'Descampado' THEN
                rand_num := random() * 100;
                IF rand_num <= 35.00 THEN
                    CALL inserir_inst_mob('ghast', 10, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;

                rand_num := random() * 100;
                IF rand_num <= 50.00 THEN
                    CALL inserir_inst_mob('piglin zumbi', 20, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;
            END IF;

            -- enderman (spawn em Floresta distorcida)
            IF chunk_rec.nome_bioma = 'Floresta distorcida' THEN
                rand_num := random() * 100;
                IF rand_num <= 90.00 THEN
                    CALL inserir_inst_mob('enderman', 40, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;
            END IF;
        END IF;

        -- Fim
        IF chunk_rec.nome_mapa = 'Fim' THEN
            IF chunk_rec.nome_bioma = 'Ilha do fim' THEN
                rand_num := random() * 100;
                IF rand_num <= 90.00 THEN
                    CALL inserir_inst_mob('enderman', 40, chunk_rec.numero, chunk_rec.nome_mapa, NULL);
                END IF;
            END IF;
        END IF;

    END LOOP;
END
$$;

-- Tabela Instância Fonte
DO
$$
DECLARE
    chunk_rec RECORD;
    rand_num FLOAT;
BEGIN
    -- Iterando por todos os chunks na tabela Chunk
    FOR chunk_rec IN 
        SELECT numero, nome_bioma, nome_mapa 
        FROM Chunk
    LOOP
        -- Superfície
        IF chunk_rec.nome_mapa = 'Superfície' THEN
            -- Árvore (gerada em Floresta e Selva, raramente em Planícies)
            IF chunk_rec.nome_bioma IN ('Floresta', 'Selva') THEN
                rand_num := random() * 100;
                IF rand_num <= 70.00 THEN
                    CALL inserir_inst_fonte('Árvore', 24, chunk_rec.numero, chunk_rec.nome_mapa);
                END IF;
            ELSIF chunk_rec.nome_bioma = 'Planície' THEN
                rand_num := random() * 100;
                IF rand_num <= 10.00 THEN
                    CALL inserir_inst_fonte('Árvore', 24, chunk_rec.numero, chunk_rec.nome_mapa);
                END IF;
            END IF;

            -- Pedreira (gerada raramente em todos os biomas, mais comumente em Montanhas)
            rand_num := random() * 100;
            IF chunk_rec.nome_bioma = 'Montanha' THEN
                IF rand_num <= 50.00 THEN
                    CALL inserir_inst_fonte('Pedreira', 16, chunk_rec.numero, chunk_rec.nome_mapa);
                END IF;
            ELSE
                IF rand_num <= 15.00 THEN  -- Raramente em outros biomas
                    CALL inserir_inst_fonte('Pedreira', 16, chunk_rec.numero, chunk_rec.nome_mapa);
                END IF;
            END IF;

            -- Duna e Campo de Cana de Açúcar (gerada no Deserto)
            IF chunk_rec.nome_bioma = 'Deserto' THEN
                rand_num := random() * 100;
                IF rand_num <= 50.00 THEN
                    CALL inserir_inst_fonte('Duna', 16, chunk_rec.numero, chunk_rec.nome_mapa);
                END IF;

                rand_num := random() * 100;
                IF rand_num <= 30.00 THEN
                    CALL inserir_inst_fonte('Campo de Cana de Açúcar', 5, chunk_rec.numero, chunk_rec.nome_mapa);
                END IF;
            END IF;

            -- Cardume (gerado no Lago)
            IF chunk_rec.nome_bioma = 'Lago' THEN
                rand_num := random() * 100;
                IF rand_num <= 60.00 THEN
                    CALL inserir_inst_fonte('Cardume', 5, chunk_rec.numero, chunk_rec.nome_mapa);
                END IF;
            END IF;

            -- Jazida de Carvão (gerada nas Montanhas)
            IF chunk_rec.nome_bioma = 'Montanha' THEN
                rand_num := random() * 100;
                IF rand_num <= 35.00 THEN
                    CALL inserir_inst_fonte('Jazida de Carvão', 24, chunk_rec.numero, chunk_rec.nome_mapa);
                END IF;
            END IF;

        -- Cavernas
        ELSIF chunk_rec.nome_mapa = 'Cavernas' THEN
            IF chunk_rec.nome_bioma != 'Cidade ancestral' THEN
                -- Jazida de Carvão
                rand_num := random() * 100;
                IF rand_num <= 40.00 THEN
                    CALL inserir_inst_fonte('Jazida de Carvão', 24, chunk_rec.numero, chunk_rec.nome_mapa);
                END IF;

                -- Jazida de Ferro
                rand_num := random() * 100;
                IF rand_num <= 50.00 THEN
                    CALL inserir_inst_fonte('Jazida de Ferro', 10, chunk_rec.numero, chunk_rec.nome_mapa);
                END IF;

                -- Depósito de Redstone
                rand_num := random() * 100;
                IF rand_num <= 25.00 THEN
                    CALL inserir_inst_fonte('Depósito de Redstone', 16, chunk_rec.numero, chunk_rec.nome_mapa);
                END IF;

                -- Jazida de Ouro
                rand_num := random() * 100;
                IF rand_num <= 20.00 THEN
                    CALL inserir_inst_fonte('Jazida de Ouro', 8, chunk_rec.numero, chunk_rec.nome_mapa);
                END IF;

                -- Veio de Diamante
                rand_num := random() * 100;
                IF rand_num <= 10.00 THEN
                    CALL inserir_inst_fonte('Veio de Diamante', 5, chunk_rec.numero, chunk_rec.nome_mapa);
                END IF;
            END IF;

        -- Nether
        ELSIF chunk_rec.nome_mapa = 'Nether' THEN
            IF chunk_rec.nome_bioma = 'Descampado' THEN
                -- Depósito de Netherita
                rand_num := random() * 100;
                IF rand_num <= 5.00 THEN
                    CALL inserir_inst_fonte('Depósito de Netherita', 5, chunk_rec.numero, chunk_rec.nome_mapa);
                END IF;
            END IF;
        END IF;
    END LOOP;
END
$$;


-- Tabela Instância Contruivel
DO
$$
DECLARE
    chunk_rec RECORD;
    rand_num FLOAT;
    vila_existente INTEGER;
BEGIN
    -- Iterando por todos os chunks na tabela Chunk
    FOR chunk_rec IN 
        SELECT numero, nome_bioma, nome_mapa 
        FROM Chunk
    LOOP
        -- Verificar se existe uma Vila no chunk
        SELECT COUNT(*) INTO vila_existente
        FROM InstanciaEstrutura
        WHERE nome_estrutura = 'Vila' AND numero_chunk = chunk_rec.numero AND nome_mapa = chunk_rec.nome_mapa;

        -- Se houver uma Vila no chunk
        IF vila_existente > 0 THEN
            -- Fazenda
            rand_num := random() * 100;
            IF rand_num <= 30.00 THEN
                CALL inserir_inst_construivel('Fazenda', chunk_rec.numero, chunk_rec.nome_mapa);
            END IF;

            -- Fornalha
            rand_num := random() * 100;
            IF rand_num <= 10.00 THEN
                CALL inserir_inst_construivel('Fornalha', chunk_rec.numero, chunk_rec.nome_mapa);
            END IF;

            -- Biblioteca
            rand_num := random() * 100;
            IF rand_num <= 7.00 THEN
                CALL inserir_inst_construivel('Biblioteca', chunk_rec.numero, chunk_rec.nome_mapa);
            END IF;
        END IF;

        -- Portais de Viagem
        rand_num := random() * 100;
        IF rand_num <= 1.00 THEN  -- probabilidade extremamente rara
            CALL inserir_inst_construivel('Portal de Viagem', chunk_rec.numero, chunk_rec.nome_mapa);
        END IF;

    END LOOP;
END
$$;
