--------------------------------------------------------------------------------------------------------
-------------------------------- GENERALIZAÇÃO/ESPECIALIZAÇÃO DE ITENS ---------------------------------
--------------------------------------------------------------------------------------------------------

--- REMOVE A PERMISSÃO DE INSERIR DIRETAMENTE NAS TABELAS

REVOKE INSERT ON Item FROM PUBLIC;
REVOKE INSERT ON Alimento FROM PUBLIC;
REVOKE INSERT ON Craftavel FROM PUBLIC;
REVOKE INSERT ON ArmaduraDuravel FROM PUBLIC;
REVOKE INSERT ON FerramentaDuravel FROM PUBLIC;
REVOKE INSERT ON Funcional FROM PUBLIC;

--- REMOVE A PERMISSÃO DE DELETAR DIRETAMENTE NAS TABELAS ESPECÍFICAS

REVOKE DELETE ON Alimento FROM PUBLIC;
REVOKE DELETE ON Craftavel FROM PUBLIC;
REVOKE DELETE ON ArmaduraDuravel FROM PUBLIC;
REVOKE DELETE ON FerramentaDuravel FROM PUBLIC;
REVOKE DELETE ON Funcional FROM PUBLIC;

--- STORED PROCEDURE PARA INSERIR NAS TABELAS

CREATE OR REPLACE PROCEDURE inserir_item(
    p_nome VARCHAR(30),
    p_tipo_item tipo_item,
    p_pts_fome INT DEFAULT NULL,
    p_tipo_craftavel tipo_craftavel DEFAULT NULL,
    p_funcao TEXT DEFAULT NULL,
    p_durabilidade_total INT DEFAULT NULL,
    p_pts_dano INT DEFAULT NULL,
    p_pts_armadura INT DEFAULT NULL
)
AS $inserir_item$
BEGIN
    INSERT INTO Item(nome, tipo_item)
    VALUES(p_nome, p_tipo_item);

    IF p_tipo_item = 'craftavel' THEN
        INSERT INTO Craftavel(nome_item, tipo_craftavel)
        VALUES (p_nome, p_tipo_craftavel);

        IF p_tipo_craftavel = 'funcional' THEN
            INSERT INTO Funcional(nome_item, funcao)
            VALUES (p_nome, p_funcao);

        ELSIF p_tipo_craftavel = 'ferramenta' THEN
            INSERT INTO FerramentaDuravel(nome_item, durabilidade_total, pts_dano)
            VALUES (p_nome, p_durabilidade_total, p_pts_dano);

        ELSIF p_tipo_craftavel = 'armadura' THEN
            INSERT INTO ArmaduraDuravel(nome_item, pts_armadura, durabilidade_total)
            VALUES (p_nome, p_pts_armadura, p_durabilidade_total);

        ELSIF p_tipo_craftavel = 'material' THEN
            NULL;

		ELSE
        	RAISE EXCEPTION 'Tipo de item desconhecido: %. Deve ser "craftavel", "alimento" ou "material".', p_tipo_craftavel;
    	END IF;

    ELSIF p_tipo_item = 'alimento' THEN
        INSERT INTO Alimento(nome_item, pts_fome)
        VALUES (p_nome, p_pts_fome);

    ELSIF p_tipo_item = 'material' THEN
        NULL;

    ELSE
        RAISE EXCEPTION 'Tipo de item desconhecido: %. Deve ser "craftavel", "alimento" ou "material".', p_tipo_item;
    END IF;
END
$inserir_item$ LANGUAGE plpgsql SECURITY DEFINER;

--- TRIGGER E STORED PROCEDURE PARA DELETAR ITEM

CREATE OR REPLACE FUNCTION deletar_item()
RETURNS trigger 
AS $deletar_item$
BEGIN

	IF (OLD.tipo_item = 'craftavel') THEN
		DELETE FROM Craftavel
		WHERE nome_item = OLD.nome;
	END IF;

	IF (OLD.tipo_item = 'alimento') THEN
		DELETE FROM Alimento
		WHERE nome_item = OLD.nome;
	END IF;
	
	RETURN OLD;
	
END;
$deletar_item$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER deletar_item
BEFORE DELETE ON Item
FOR EACH ROW EXECUTE PROCEDURE deletar_item();

--- TRIGGER E STORED PROCEDURE PARA DELETAR ITEM CRAFTAVEL

CREATE OR REPLACE FUNCTION deletar_item_craftavel()
RETURNS trigger 
AS $deletar_item_craftavel$
BEGIN

	IF (OLD.tipo_craftavel = 'funcional') THEN
		DELETE FROM Funcional
		WHERE nome_item = OLD.nome_item;
		
	ELSIF (OLD.tipo_craftavel = 'ferramenta') THEN
		DELETE FROM FerramentaDuravel
		WHERE nome_item = OLD.nome_item;

	ELSIF (OLD.tipo_craftavel = 'armadura') THEN
		DELETE FROM ArmaduraDuravel
		WHERE nome_item = OLD.nome_item;

	ELSIF (OLD.tipo_craftavel = 'material') THEN
		NULL;

	ELSE
		RAISE EXCEPTION 'Erro ao deletar. O tipo está errado.';			
	END IF;
	
	RETURN OLD;
	
END;
$deletar_item_craftavel$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER deletar_item_craftavel
BEFORE DELETE ON Craftavel
FOR EACH ROW EXECUTE PROCEDURE deletar_item_craftavel();

--- TRIGGER E STORED PROCEDURE PARA IMPEDIR DE ATUALIZAR O TIPO DA TABELA ITEM

CREATE OR REPLACE FUNCTION prevencao_update_tipo_item()
RETURNS trigger 
AS $prevencao_update_tipo_item$
BEGIN

	IF (OLD.tipo_item <> NEW.tipo_item) THEN
		RAISE EXCEPTION 'Não é permitido alterar o tipo de item.';
	END IF;
	
	RETURN NEW;
	
END;
$prevencao_update_tipo_item$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER prevencao_update_tipo_item
BEFORE UPDATE ON Item
FOR EACH ROW EXECUTE PROCEDURE prevencao_update_tipo_item();

--- TRIGGER E STORED PROCEDURE PARA IMPEDIR DE ATUALIZAR O TIPO DA TABELA CRAFTAVEL

CREATE OR REPLACE FUNCTION prevencao_update_tipo_item_craftavel()
RETURNS trigger 
AS $prevencao_update_tipo_item_craftavel$
BEGIN

	IF (OLD.tipo_craftavel <> NEW.tipo_craftavel) THEN
		RAISE EXCEPTION 'Não é permitido alterar o tipo de item craftável.';
	END IF;
	
	RETURN NEW;
	
END;
$prevencao_update_tipo_item_craftavel$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER prevencao_update_tipo_item_craftavel
BEFORE UPDATE ON Craftavel
FOR EACH ROW EXECUTE PROCEDURE prevencao_update_tipo_item_craftavel();

--------------------------------------------------------------------------------------------------------
-------------------------------- GENERALIZAÇÃO/ESPECIALIZAÇÃO DE MOBS ----------------------------------
--------------------------------------------------------------------------------------------------------

--- REMOVE A PERMISSÃO DE INSERIR DIRETAMENTE NAS TABELAS

REVOKE INSERT ON Mob FROM PUBLIC;
REVOKE INSERT ON Agressivo FROM PUBLIC;
REVOKE INSERT ON Pacifico FROM PUBLIC;
REVOKE INSERT ON NPC FROM PUBLIC;

--- REMOVE A PERMISSÃO DE DELETAR DIRETAMENTE NAS TABELAS ESPECÍFICAS

REVOKE DELETE ON Agressivo FROM PUBLIC;
REVOKE DELETE ON Pacifico FROM PUBLIC;
REVOKE DELETE ON NPC FROM PUBLIC;

--- STORED PROCEDURE PARA INSERIR NAS TABELAS

CREATE OR REPLACE PROCEDURE inserir_mob(
	p_nome VARCHAR(30),
	p_tipo_mob tipo_mob,
	p_impulsivo BOOLEAN DEFAULT NULL,
	p_pts_dano INT DEFAULT NULL,
	p_vida_max INT DEFAULT NULL,
	p_tipo_pacifico tipo_pacifico DEFAULT NULL
)
AS $inserir_mob$
BEGIN
	INSERT INTO Mob(nome, tipo_mob)
	VALUES(p_nome, p_tipo_mob);

	IF p_tipo_mob = 'pacifico' THEN
		INSERT INTO Pacifico(nome_mob, vida_max, tipo_pacifico)
		VALUES(p_nome, p_vida_max, p_tipo_pacifico);

		IF p_tipo_pacifico = 'NPC' THEN
			INSERT INTO NPC(nome_pacifico)
			VALUES(p_nome);

		ELSIF p_tipo_pacifico = 'outro' THEN
			NULL;

		ELSE
        	RAISE EXCEPTION 'Tipo de mob pacifico desconhecido: %. Deve ser "NPC" ou "outro".', p_tipo_pacifico;
		END IF;

	ELSIF p_tipo_mob = 'agressivo' THEN
		INSERT INTO Agressivo(nome_mob, impulsivo, pts_dano, vida_max)
		VALUES(p_nome, p_impulsivo, p_pts_dano, p_vida_max);

	ELSE
		RAISE EXCEPTION 'Tipo de mob desconhecido: %. Deve ser "pacifico" ou "agressivo".', p_tipo_mob;
	END IF;
END
$inserir_mob$ LANGUAGE plpgsql SECURITY DEFINER;

--- TRIGGER E STORED PROCEDURE PARA DELETAR MOB

CREATE OR REPLACE FUNCTION deletar_mob()
RETURNS trigger 
AS $deletar_mob$
BEGIN

	IF (OLD.tipo_mob = 'pacifico') THEN
		DELETE FROM Pacifico
		WHERE nome_mob = OLD.nome;
	END IF;

	IF (OLD.tipo_mob = 'agressivo') THEN
		DELETE FROM Agressivo
		WHERE nome_mob = OLD.nome;
	END IF;
	
	RETURN OLD;
	
END;
$deletar_mob$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER deletar_mob
BEFORE DELETE ON Mob
FOR EACH ROW EXECUTE PROCEDURE deletar_mob();

--- TRIGGER E STORED PROCEDURE PARA DELETAR MOB PACIFICO

CREATE OR REPLACE FUNCTION deletar_mob_pacifico()
RETURNS trigger 
AS $deletar_mob_pacifico$
BEGIN

	IF (OLD.tipo_mob = 'NPC') THEN
		DELETE FROM Pacifico
		WHERE nome_pacifico = OLD.nome_mob;

	ELSIF (OLD.tipo_mob = 'outro') THEN
		NULL;
	
	ELSE
		RAISE EXCEPTION 'Erro ao deletar. O tipo está errado.';			
	END IF;
	
	RETURN OLD;
	
END;
$deletar_mob_pacifico$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER deletar_mob_pacifico
BEFORE DELETE ON Pacifico
FOR EACH ROW EXECUTE PROCEDURE deletar_mob_pacifico();

--- TRIGGER E STORED PROCEDURE PARA IMPEDIR DE ATUALIZAR O TIPO DA TABELA MOB

CREATE OR REPLACE FUNCTION prevencao_update_tipo_mob()
RETURNS trigger 
AS $prevencao_update_tipo_mob$
BEGIN

	IF (OLD.tipo_mob <> NEW.tipo_mob) THEN
		RAISE EXCEPTION 'Não é permitido alterar o tipo de mob.';
	END IF;
	
	RETURN NEW;
	
END;
$prevencao_update_tipo_mob$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER prevencao_update_tipo_mob
BEFORE UPDATE ON Mob
FOR EACH ROW EXECUTE PROCEDURE prevencao_update_tipo_mob();

--- TRIGGER E STORED PROCEDURE PARA IMPEDIR DE ATUALIZAR O TIPO DA TABELA PACIFICO

CREATE OR REPLACE FUNCTION prevencao_update_tipo_pacifico()
RETURNS trigger 
AS $prevencao_update_tipo_pacifico$
BEGIN

	IF (OLD.tipo_pacifico <> NEW.tipo_pacifico) THEN
		RAISE EXCEPTION 'Não é permitido alterar o tipo de mob pacífico.';
	END IF;
	
	RETURN NEW;
	
END;
$prevencao_update_tipo_pacifico$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER prevencao_update_tipo_pacifico
BEFORE UPDATE ON Pacifico
FOR EACH ROW EXECUTE PROCEDURE prevencao_update_tipo_pacifico();

--- CHECAR EXISTÊNCIA NA TABELA PACIFICO

CREATE OR REPLACE FUNCTION check_existe_pacifico() RETURNS trigger 
AS $check_existe_pacifico$
BEGIN
	PERFORM * FROM Pacifico WHERE nome_mob = NEW.nome_mob;
	IF FOUND THEN
		RAISE EXCEPTION 'Este mob já existe na tabela Pacifico.';
	END IF;
	
	RETURN NEW;
END;
$check_existe_pacifico$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER check_existe_pacifico
BEFORE INSERT ON Agressivo
FOR EACH ROW EXECUTE PROCEDURE check_existe_pacifico();

--- CHECAR EXISTÊNCIA NA TABELA AGRESSIVO

CREATE OR REPLACE FUNCTION check_existe_agressivo() RETURNS trigger 
AS $check_existe_agressivo$
BEGIN
	PERFORM * FROM Agressivo WHERE nome_mob = NEW.nome_mob;
	IF FOUND THEN
		RAISE EXCEPTION 'Este mob já existe na tabela Agressivo.';
	END IF;
	
	RETURN NEW;
END;
$check_existe_agressivo$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER check_existe_agressivo
BEFORE INSERT ON Pacifico
FOR EACH ROW EXECUTE PROCEDURE check_existe_agressivo();

--- CHECAR INSERÇÃO DA VIDA DO MOB NA TABELA 

CREATE OR REPLACE FUNCTION checar_vida_mob() RETURNS trigger 
AS $checar_vida_mob$
BEGIN

    DECLARE 
        tipo_mob VARCHAR(30);
        vida_max INT;
    BEGIN

        SELECT m.tipo_mob
        INTO tipo_mob
        FROM Mob m
        WHERE m.nome = NEW.nome_mob;

        IF tipo_mob = 'agressivo' THEN
            
            SELECT a.vida_max 
            INTO vida_max
            FROM Agressivo a
            WHERE a.nome_mob = NEW.nome_mob;
            
            IF NEW.vida_atual > vida_max THEN
                RAISE EXCEPTION 'A vida atual (%) não pode ser maior que a vida máxima (%) para o mob agressivo %.', 
                    NEW.vida_atual, vida_max, NEW.nome_mob;
            END IF;

        ELSIF tipo_mob = 'pacifico' THEN

            SELECT p.vida_max 
            INTO vida_max
            FROM Pacifico p
            WHERE p.nome_mob = NEW.nome_mob;
            
            IF NEW.vida_atual > vida_max THEN
                RAISE EXCEPTION 'A vida atual (%) não pode ser maior que a vida máxima (%) para o mob pacífico %.', 
                    NEW.vida_atual, vida_max, NEW.nome_mob;
            END IF;

        ELSE 
			RAISE EXCEPTION 'Tipo de mob % não é válido.', tipo_mob;
		END IF;

		RETURN NEW;
    END;
END;
$checar_vida_mob$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER checar_vida_mob
BEFORE INSERT OR UPDATE ON InstanciaMob
FOR EACH ROW
EXECUTE FUNCTION checar_vida_mob();

--------------------------------------------------------------------------------------------------------
---------------------------------- MANIPULAÇÃO DE TABELAS INSTÂNCIA ------------------------------------
--------------------------------------------------------------------------------------------------------

--- INSERIR INSTÂNCIA DE MOB

CREATE OR REPLACE PROCEDURE inserir_inst_mob(
    nome_mob VARCHAR,
    vida_atual INT,
    numero_chunk INT,
    nome_mapa VARCHAR,
    id_estrutura INT
)
AS $$
BEGIN
    -- Inserir o mob na tabela InstanciaMob
    INSERT INTO InstanciaMob (nome_mob, vida_atual, numero_chunk, nome_mapa, id_estrutura)
    VALUES (nome_mob, vida_atual, numero_chunk, nome_mapa, id_estrutura);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

--- INSERIR INSTÂNCIA DE ESTRUTURA

CREATE OR REPLACE PROCEDURE inserir_inst_estrutura(
    nome_estrutura VARCHAR,
    nome_bioma VARCHAR,
    numero_chunk INT,
    nome_mapa VARCHAR,
    OUT nova_estrutura_id INT
)
AS $$
BEGIN
    -- Inserir a estrutura na tabela InstanciaEstrutura
    INSERT INTO InstanciaEstrutura (nome_estrutura, nome_bioma, numero_chunk, nome_mapa)
    VALUES (nome_estrutura, nome_bioma, numero_chunk, nome_mapa)
    RETURNING id_inst_estrutura INTO nova_estrutura_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

--- INSERIR INSTÂNCIA DE FONTE

CREATE OR REPLACE PROCEDURE inserir_inst_fonte(
    nome_fonte VARCHAR, 
    qtd_atual INT, 
    numero_chunk INT, 
    nome_mapa VARCHAR
)
AS $$
BEGIN
    -- Inserir uma instância de fonte no chunk
    INSERT INTO InstanciaFonte (nome_fonte, qtd_atual, numero_chunk, nome_mapa)
    VALUES (nome_fonte, qtd_atual, numero_chunk, nome_mapa);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

--- INSERIR INSTÂNCIA DE CONSTRUÍVEL

CREATE OR REPLACE PROCEDURE inserir_inst_construivel(
    nome_construivel VARCHAR,
    numero_chunk INT,
    nome_mapa VARCHAR
)
AS
$$
BEGIN
    -- Inserir instância do construível
    INSERT INTO InstanciaConstruivel (nome_construivel, numero_chunk, nome_mapa)
    VALUES (nome_construivel, numero_chunk, nome_mapa);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

--------------------------------------------------------------------------------------------------------
------------------------------------ PROCEDURES PARA A GAMEPLAY  ---------------------------------------
--------------------------------------------------------------------------------------------------------

--- SPAWN DE MOBS AGRESSIVOS NA SUPERFÍCIE AO ANOITECER
CREATE OR REPLACE PROCEDURE spawn_mobs_agressivos() 
AS $$
DECLARE
    chunk_rec RECORD;
    rand_num FLOAT;
BEGIN
    -- Iterando por todos os chunks no mapa "Superfície" para spawnar mobs agressivos à noite
    FOR chunk_rec IN 
        SELECT numero, nome_bioma 
        FROM Chunk
        WHERE nome_mapa = 'Superfície'
    LOOP
        -- Zumbi (spawn em Planície, Floresta, Pântano e Deserto)
        IF chunk_rec.nome_bioma IN ('Planície', 'Floresta', 'Pântano', 'Deserto') THEN
            rand_num := random() * 100;
            IF rand_num <= 70.00 THEN
                CALL inserir_inst_mob('Zumbi', 20, chunk_rec.numero, 'Superfície', NULL);
            END IF;
        END IF;

        -- Esqueleto (spawn em Planície, Montanha, Floresta e Deserto)
        IF chunk_rec.nome_bioma IN ('Planície', 'Montanha', 'Floresta', 'Deserto') THEN
            rand_num := random() * 100;
            IF rand_num <= 60.00 THEN
                CALL inserir_inst_mob('Esqueleto', 20, chunk_rec.numero, 'Superfície', NULL);
            END IF;
        END IF;

        -- Aranha (spawn em Floresta, Pântano e Deserto)
        IF chunk_rec.nome_bioma IN ('Floresta', 'Pântano', 'Deserto') THEN
            rand_num := random() * 100;
            IF rand_num <= 50.00 THEN
                CALL inserir_inst_mob('Aranha', 16, chunk_rec.numero, 'Superfície', NULL);
            END IF;
        END IF;

        -- Enderman (spawn em Planície, Deserto)
        IF chunk_rec.nome_bioma IN ('Planície', 'Deserto') THEN
            rand_num := random() * 100;
            IF rand_num <= 10.00 THEN
                CALL inserir_inst_mob('Enderman', 40, chunk_rec.numero, 'Superfície', NULL);
            END IF;
        END IF;

        -- Creeper (spawn em Floresta, Planície e Deserto)
        IF chunk_rec.nome_bioma IN ('Floresta', 'Planície', 'Deserto') THEN
            rand_num := random() * 100;
            IF rand_num <= 30.00 THEN
                CALL inserir_inst_mob('Creeper', 20, chunk_rec.numero, 'Superfície', NULL);
            END IF;
        END IF;

        -- Bruxa (spawn em Pântano)
        IF chunk_rec.nome_bioma = 'Pântano' THEN
            rand_num := random() * 100;
            IF rand_num <= 7.00 THEN
                CALL inserir_inst_mob('Bruxa', 26, chunk_rec.numero, 'Superfície', NULL);
            END IF;
        END IF;

        -- Saqueador (spawn em Planície, Montanha e Deserto)
        IF chunk_rec.nome_bioma IN ('Planície', 'Montanha', 'Deserto') THEN
            rand_num := random() * 100;
            IF rand_num <= 10.00 THEN
                CALL inserir_inst_mob('Saqueador', 24, chunk_rec.numero, 'Superfície', NULL);
            END IF;
        END IF;

    END LOOP;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

--- DESPAWN DE MOBS AGRESSIVOS NA SUPERFÍCIE AO AMANHECER, APENAS MOBS FORA DE ESTRUTURAS
CREATE OR REPLACE PROCEDURE despawn_mobs_agressivos() 
AS $$
BEGIN
    DELETE FROM InstanciaMob
    WHERE nome_mob IN ('Zumbi', 'Esqueleto', 'Aranha', 'Enderman', 'Creeper', 'Bruxa', 'Saqueador')
    AND nome_mapa = 'Superfície'
    AND id_estrutura IS NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ATUALIZAÇÃO DO CICLO DO DIA
CREATE OR REPLACE PROCEDURE atualizar_ciclo_dia() 
AS 
$$
DECLARE
    hora_atual ciclo_dia;  -- Declara uma variável para armazenar o valor atual da hora
BEGIN
    -- Atualiza o ciclo do dia apenas para o mapa 'Superficie'
    UPDATE Mapa
    SET hora = CASE
        WHEN hora = 'dia' THEN 'tarde'::ciclo_dia
        WHEN hora = 'tarde' THEN 'noite'::ciclo_dia
        WHEN hora = 'noite' THEN 'dia'::ciclo_dia
        ELSE 'dia'::ciclo_dia
    END
    WHERE nome = 'Superfície'
    RETURNING hora INTO hora_atual;  -- Armazena a hora atualizada na variável

    -- Verifica o novo ciclo do dia e executa as ações apropriadas
    IF hora_atual = 'noite' THEN
        -- Se for noite, spawna mobs agressivos
        CALL  spawn_mobs_agressivos();
    ELSIF hora_atual = 'dia' THEN
        -- Se for dia, remove mobs agressivos
        CALL  despawn_mobs_agressivos();
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

--- FUNCTION PARA MOVER JOGADOR

CREATE OR REPLACE FUNCTION mover_jogador(
    p_nomeUser VARCHAR(30),
    p_direcao VARCHAR(30),
    p_novo_chunk INT
) RETURNS TEXT
AS $mover_jogador$
BEGIN
    IF p_novo_chunk IS NOT NULL THEN
        -- Verifica se a direção é "baixo"
        IF p_direcao = 'baixo' THEN
            -- Atualiza o nome_mapa para "Cavernas"
            UPDATE Jogador
            SET nome_mapa = 'Cavernas'
            WHERE nome = p_nomeUser;

            -- Retorna uma mensagem de sucesso
            RETURN 'Você se desceu para as Cavernas e agora está no chunk ' || p_novo_chunk || '.';

        -- Verifica se a direção é "cima"
        ELSIF p_direcao = 'cima' THEN
            -- Atualiza o nome_mapa para "Superfície"
            UPDATE Jogador
            SET nome_mapa = 'Superfície'
            WHERE nome = p_nomeUser;

            -- Retorna uma mensagem de sucesso
            RETURN 'Você retornou para a Superfície e agora está no chunk ' || p_novo_chunk || '.';

        -- Caso contrário, atualiza o chunk
        ELSE
            -- Atualiza o numero_chunk
            UPDATE Jogador
            SET numero_chunk = p_novo_chunk
            WHERE nome = p_nomeUser;

            -- Retorna uma mensagem de sucesso
            RETURN 'Você se moveu para o ' || p_direcao || ' e agora está no chunk ' || p_novo_chunk || '.';
            
        END IF;

    ELSE
        RETURN 'Não é possível ir para ' || p_direcao || '.';
    END IF;
END;
$mover_jogador$ LANGUAGE plpgsql SECURITY DEFINER;

--- TRIGGER/STORED PROCEDURE PARA NÃO PERMITIR INSERIR VALOR NULO NO CHUNK DO JOGADOR

CREATE OR REPLACE FUNCTION verificar_chunk_jogador()
RETURNS TRIGGER 
AS $verificar_chunk_jogador$
BEGIN

    IF NEW.numero_chunk IS NULL THEN
        RAISE EXCEPTION 'O campo "numero_chunk" não pode ser NULL.';
    END IF;

    RETURN NEW;
END;
$verificar_chunk_jogador$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER verificar_chunk_jogador
BEFORE UPDATE ON Jogador
FOR EACH ROW
EXECUTE FUNCTION verificar_chunk_jogador();

--- FUNCTION PARA VER MOBS

CREATE OR REPLACE FUNCTION ver_mob(
    p_nomeUser VARCHAR(30),
    p_nomeMob VARCHAR(30)
) 
RETURNS TABLE (
    nome_mob VARCHAR(30),
    tipo_mob tipo_mob,
    vida_max INT,
    vida_atual INT,
    pts_dano INT
)
AS $ver_mob$
BEGIN
    RETURN QUERY
    SELECT 
        Mob.nome AS nome_mob, 
        Mob.tipo_mob, 
        COALESCE(Agressivo.vida_max, Pacifico.vida_max) AS vida_max,  -- Seleciona a vida_max de Agressivo ou Pacifico
        InstanciaMob.vida_atual, 
        Agressivo.pts_dano  -- Pega pts_dano apenas para mobs agressivos
    FROM InstanciaMob
    JOIN Mob ON InstanciaMob.nome_mob = Mob.nome
    LEFT JOIN Agressivo ON Mob.nome = Agressivo.nome_mob
    LEFT JOIN Pacifico ON Mob.nome = Pacifico.nome_mob
    WHERE InstanciaMob.nome_mob = p_nomeMob
    AND InstanciaMob.numero_chunk = (
        SELECT numero_chunk FROM Jogador WHERE nome = p_nomeUser
    );
END;
$ver_mob$ LANGUAGE plpgsql SECURITY DEFINER;

--- FUNCTION PARA CRAFTAR ITENS

CREATE OR REPLACE FUNCTION craftar_item(
    p_nomeUser VARCHAR(30), 
    p_nomeItem VARCHAR(30)
) 
RETURNS TEXT
AS $craftar_item$
DECLARE
    v_id_jogador INT;
    v_receita RECORD;
    v_itens_necessarios TEXT[];
    v_quantidade_saida INT;
    v_item VARCHAR(30);
    v_qtd_necessaria INT;
    v_qtd_no_inventario INT;
    v_id_inst_item INT;
    v_durabilidade_total INT;
    v_item_removido INT;
    v_itens_remover RECORD;
BEGIN
    -- Verificar se o item é craftável
    IF NOT EXISTS (SELECT 1 FROM Craftavel WHERE nome_item = p_nomeItem) THEN
        RETURN 'Item ' || p_nomeItem || ' não pode ser craftado.';
    END IF;

    -- Consultar a receita do item na tabela ReceitaItem
    SELECT item_1, item_2, item_3, item_4, item_5, item_6, item_7, item_8, item_9, quantidade
    INTO v_receita
    FROM ReceitaItem
    WHERE nome_item = p_nomeItem;

    IF v_receita IS NULL THEN
        RETURN 'Receita para ' || p_nomeItem || ' não encontrada.';
    END IF;

    -- Guardar os itens da receita e a quantidade de saída
    v_itens_necessarios := ARRAY[v_receita.item_1, v_receita.item_2, v_receita.item_3, v_receita.item_4, 
                                 v_receita.item_5, v_receita.item_6, v_receita.item_7, v_receita.item_8, 
                                 v_receita.item_9];
    v_itens_necessarios := array_remove(v_itens_necessarios, NULL); -- Remove NULLs da receita
    v_quantidade_saida := v_receita.quantidade;

    -- Pegar o id do jogador
    SELECT id_jogador INTO v_id_jogador FROM Jogador WHERE nome = p_nomeUser;

    IF v_id_jogador IS NULL THEN
        RETURN 'Jogador ' || p_nomeUser || ' não encontrado.';
    END IF;

    -- Verificar se o jogador tem todos os materiais necessários
    FOR v_itens_remover IN (SELECT DISTINCT unnest(v_itens_necessarios) AS item) LOOP
        v_item := v_itens_remover.item;

        -- Contar quantas vezes esse item específico aparece na receita
        v_qtd_necessaria := (SELECT COUNT(*) FROM unnest(v_itens_necessarios) x WHERE x = v_item);

        -- Verificar a quantidade disponível no inventário
        SELECT COUNT(*) INTO v_qtd_no_inventario
        FROM Inventario
        JOIN InstanciaItem ON Inventario.id_inst_item = InstanciaItem.id_inst_item
        WHERE Inventario.id_inventario = v_id_jogador
        AND InstanciaItem.nome_item = v_item;

        -- Comparar a quantidade disponível com a quantidade necessária
        IF v_qtd_no_inventario < v_qtd_necessaria THEN
            RETURN 'Você não tem materiais suficientes para craftar ' || p_nomeItem || '. Faltam ' || (v_qtd_necessaria - v_qtd_no_inventario) || ' unidades de ' || v_item || '.';
        END IF;
    END LOOP;

    -- Remover os itens do inventário necessários para o craft (somente a quantidade exata para um craft)
    FOR v_itens_remover IN (SELECT DISTINCT unnest(v_itens_necessarios) AS item) LOOP
        v_item := v_itens_remover.item;
        v_qtd_necessaria := (SELECT COUNT(*) FROM unnest(v_itens_necessarios) x WHERE x = v_item);

        -- Remover exatamente a quantidade necessária do inventário
        v_item_removido := 0; -- Inicia um contador para itens removidos
        FOR i IN 1..v_qtd_necessaria LOOP
            -- Encontrar o id_inst_item para cada item e remover
            SELECT id_inst_item INTO v_id_inst_item 
            FROM InstanciaItem 
            WHERE nome_item = v_item 
            AND id_inst_item IN (SELECT id_inst_item FROM Inventario WHERE id_inventario = v_id_jogador)
            ORDER BY id_inst_item
            LIMIT 1;

            -- Remover do inventário e da instância
            IF v_id_inst_item IS NOT NULL THEN
                DELETE FROM Inventario WHERE id_inst_item = v_id_inst_item;
                DELETE FROM InstanciaItem WHERE id_inst_item = v_id_inst_item;
                v_item_removido := v_item_removido + 1; -- Incrementa a contagem de itens removidos
            END IF;

            -- Se já removemos a quantidade necessária de itens, saímos do loop
            IF v_item_removido >= v_qtd_necessaria THEN
                EXIT;
            END IF;
        END LOOP;
    END LOOP;

    -- Verificar se o item a ser craftado tem durabilidade (FerramentaDuravel ou ArmaduraDuravel)
    IF EXISTS (SELECT 1 FROM FerramentaDuravel WHERE nome_item = p_nomeItem) THEN
        -- Se for ferramenta durável, pegar a durabilidade total
        SELECT durabilidade_total INTO v_durabilidade_total FROM FerramentaDuravel WHERE nome_item = p_nomeItem;
    ELSIF EXISTS (SELECT 1 FROM ArmaduraDuravel WHERE nome_item = p_nomeItem) THEN
        -- Se for armadura durável, pegar a durabilidade total
        SELECT durabilidade_total INTO v_durabilidade_total FROM ArmaduraDuravel WHERE nome_item = p_nomeItem;
    ELSE
        -- Caso o item não tenha durabilidade, definir como NULL
        v_durabilidade_total := NULL;
    END IF;

    -- Criar e adicionar o novo item craftado ao inventário do jogador
    FOR i IN 1..v_quantidade_saida LOOP
        INSERT INTO InstanciaItem (nome_item, durabilidade_atual) 
        VALUES (p_nomeItem, v_durabilidade_total) 
        RETURNING id_inst_item INTO v_id_inst_item;

        INSERT INTO Inventario (id_inst_item, id_inventario)
        VALUES (v_id_inst_item, v_id_jogador);
    END LOOP;

    -- Retorna mensagem de sucesso
    RETURN 'Item ' || p_nomeItem || ' craftado com sucesso e adicionado ao inventário.';
END;
$craftar_item$ LANGUAGE plpgsql SECURITY DEFINER;


--- FUNCTION PARA CONSTRUIR CONSTRUÇÃO

CREATE OR REPLACE FUNCTION construir_construcao(nome_jogador VARCHAR, nome_construcao VARCHAR)
RETURNS TEXT AS $construir_construcao$
DECLARE
    chunk_atual INT;
    mapa_atual VARCHAR(30);
    construcao_existente RECORD;
    receita_itens RECORD;
    quantidade_no_inventario INT;
    novo_portal_chunk_nether INT;
    v_qtd_remover INT;
    v_id_inst_item INT;
BEGIN
    -- 1. Obter a posição atual do jogador (chunk atual e mapa)
    SELECT Jogador.numero_chunk, Jogador.nome_mapa
    INTO chunk_atual, mapa_atual
    FROM Jogador
    WHERE Jogador.nome = nome_jogador;

    -- Verifica se o jogador foi encontrado
    IF NOT FOUND THEN
        RETURN 'Jogador não encontrado.';
    END IF;

    -- 2. Verificar se a construção já existe no chunk
    SELECT 1
    INTO construcao_existente
    FROM InstanciaConstruivel
    WHERE nome_construivel = nome_construcao
      AND numero_chunk = chunk_atual
      AND nome_mapa = mapa_atual;

    -- Se a construção já existir, lançar uma exceção
    IF FOUND THEN
        RETURN 'Já existe ' || nome_construcao || ' nesse chunk.';
    END IF;

    -- 3. Verificar se o nome da construção está presente na tabela Construivel
    IF nome_construcao = 'Portal do Nether' THEN
        -- Inserir "Portal do Nether" na tabela Construivel se não estiver lá
        IF NOT EXISTS (SELECT 1 FROM Construivel WHERE nome = 'Portal do Nether') THEN
            INSERT INTO Construivel (nome, descricao) VALUES ('Portal do Nether', 'Um portal para o Nether.');
        END IF;
    END IF;

    -- 4. Obter a receita da construção
    FOR receita_itens IN
        SELECT item, quantidade
        FROM ReceitaConstruivel
        WHERE nome_construivel = nome_construcao
    LOOP
        -- 5. Verificar se o jogador tem os itens necessários
        SELECT COUNT(*) INTO quantidade_no_inventario
        FROM Inventario
        JOIN InstanciaItem ON Inventario.id_inst_item = InstanciaItem.id_inst_item
        WHERE InstanciaItem.nome_item = receita_itens.item
          AND Inventario.id_inventario = (SELECT id_jogador FROM Jogador WHERE nome = nome_jogador);

        -- Se o jogador não tiver o item ou quantidade insuficiente
        IF quantidade_no_inventario < receita_itens.quantidade THEN
            RETURN 'Você não possui itens suficientes para construir ' || nome_construcao || '.';
        END IF;
    END LOOP;

    -- 5. Inserir a nova construção no chunk
    INSERT INTO InstanciaConstruivel (nome_construivel, numero_chunk, nome_mapa)
    VALUES (nome_construcao, chunk_atual, mapa_atual);

    -- 6. Se for um "Portal do Nether", criar um portal correspondente no Nether
    IF nome_construcao = 'Portal do Nether' THEN
        -- Gerar um chunk aleatório no mapa "Nether"
        INSERT INTO InstanciaConstruivel (nome_construivel, numero_chunk, nome_mapa)
        VALUES ('Portal do Nether', (SELECT FLOOR(random() * 900) + 1), 'Nether')
        RETURNING numero_chunk INTO novo_portal_chunk_nether;

        -- Garantir que o chunk no Nether existe na tabela Chunk
        INSERT INTO Chunk (numero, nome_bioma, nome_mapa)
        VALUES (novo_portal_chunk_nether, 'BiomaDesconhecido', 'Nether')
        ON CONFLICT DO NOTHING;
    END IF;

    -- 7. Remover os itens usados do inventário de acordo com a quantidade exata necessária
    FOR receita_itens IN
        SELECT item, quantidade
        FROM ReceitaConstruivel
        WHERE nome_construivel = nome_construcao
    LOOP
        v_qtd_remover := receita_itens.quantidade;

        -- Remover exatamente a quantidade necessária de cada item
        FOR i IN 1..v_qtd_remover LOOP
            -- Encontrar o id_inst_item para o item específico e removê-lo
            SELECT id_inst_item INTO v_id_inst_item
            FROM InstanciaItem
            WHERE nome_item = receita_itens.item
              AND id_inst_item IN (SELECT id_inst_item FROM Inventario WHERE id_inventario = (SELECT id_jogador FROM Jogador WHERE nome = nome_jogador))
            LIMIT 1;

            -- Remover do inventário e da instância
            DELETE FROM Inventario WHERE id_inst_item = v_id_inst_item;
            DELETE FROM InstanciaItem WHERE id_inst_item = v_id_inst_item;
        END LOOP;
    END LOOP;

    -- Retornar sucesso para a construção (após a remoção dos itens)
    IF nome_construcao = 'Portal do Nether' THEN
        RETURN 'Um novo portal foi criado no Nether, no chunk ' || novo_portal_chunk_nether || '.';
    ELSE
        RETURN 'Você construiu ' || nome_construcao || ' com sucesso!';
    END IF;

END;
$construir_construcao$ LANGUAGE plpgsql SECURITY DEFINER;
