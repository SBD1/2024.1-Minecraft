--------------------------------------------------------------------------------------------------------
-------------------------------- Generalização/Especialização dos itens --------------------------------
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
$inserir_item$ LANGUAGE plpgsql;

--- TRIGGER E STORED PROCEDURE PARA DELETAR ITEM

CREATE OR REPLACE FUNCTION deletar_item()
RETURNS trigger AS $deletar_item$
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

$deletar_item$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER deletar_item
BEFORE DELETE ON Item
FOR EACH ROW EXECUTE PROCEDURE deletar_item();

--- TRIGGER E STORED PROCEDURE PARA DELETAR ITEM CRAFTAVEL

CREATE OR REPLACE FUNCTION deletar_item_craftavel()
RETURNS trigger AS $deletar_item_craftavel$
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

$deletar_item_craftavel$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER deletar_item_craftavel
BEFORE DELETE ON Craftavel
FOR EACH ROW EXECUTE PROCEDURE deletar_item_craftavel();

--- TRIGGER E STORED PROCEDURE PARA IMPEDIR DE ATUALIZAR O TIPO DA TABELA ITEM

CREATE OR REPLACE FUNCTION prevencao_update_tipo_item()
RETURNS trigger AS $prevencao_update_tipo_item$
BEGIN

	IF (OLD.tipo_item <> NEW.tipo_item) THEN
		RAISE EXCEPTION 'Não é permitido alterar o tipo de item.';
	END IF;
	
	RETURN NEW;
	
END;

$prevencao_update_tipo_item$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER prevencao_update_tipo_item
BEFORE UPDATE ON Item
FOR EACH ROW EXECUTE PROCEDURE prevencao_update_tipo_item();

--- TRIGGER E STORED PROCEDURE PARA IMPEDIR DE ATUALIZAR O TIPO DA TABELA CRAFTAVEL

CREATE OR REPLACE FUNCTION prevencao_update_tipo_item_craftavel()
RETURNS trigger AS $prevencao_update_tipo_item_craftavel$
BEGIN

	IF (OLD.tipo_craftavel <> NEW.tipo_craftavel) THEN
		RAISE EXCEPTION 'Não é permitido alterar o tipo de item craftável.';
	END IF;
	
	RETURN NEW;
	
END;

$prevencao_update_tipo_item_craftavel$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER prevencao_update_tipo_item_craftavel
BEFORE UPDATE ON Craftavel
FOR EACH ROW EXECUTE PROCEDURE prevencao_update_tipo_item_craftavel();

--------------------------------------------------------------------------------------------------------
-------------------------------- Generalização/Especialização dos mobs --------------------------------
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
$inserir_mob$ LANGUAGE plpgsql;

--- TRIGGER E STORED PROCEDURE PARA DELETAR MOB

CREATE OR REPLACE FUNCTION deletar_mob()
RETURNS trigger AS $deletar_mob$
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

$deletar_mob$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER deletar_mob
BEFORE DELETE ON Mob
FOR EACH ROW EXECUTE PROCEDURE deletar_mob();

--- TRIGGER E STORED PROCEDURE PARA DELETAR MOB PACIFICO

CREATE OR REPLACE FUNCTION deletar_mob_pacifico()
RETURNS trigger AS $deletar_mob_pacifico$
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

$deletar_mob_pacifico$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER deletar_mob_pacifico
BEFORE DELETE ON Pacifico
FOR EACH ROW EXECUTE PROCEDURE deletar_mob_pacifico();

--- TRIGGER E STORED PROCEDURE PARA IMPEDIR DE ATUALIZAR O TIPO DA TABELA MOB

CREATE OR REPLACE FUNCTION prevencao_update_tipo_mob()
RETURNS trigger AS $prevencao_update_tipo_mob$
BEGIN

	IF (OLD.tipo_mob <> NEW.tipo_mob) THEN
		RAISE EXCEPTION 'Não é permitido alterar o tipo de mob.';
	END IF;
	
	RETURN NEW;
	
END;

$prevencao_update_tipo_mob$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER prevencao_update_tipo_mob
BEFORE UPDATE ON Mob
FOR EACH ROW EXECUTE PROCEDURE prevencao_update_tipo_mob();

--- TRIGGER E STORED PROCEDURE PARA IMPEDIR DE ATUALIZAR O TIPO DA TABELA PACIFICO

CREATE OR REPLACE FUNCTION prevencao_update_tipo_pacifico()
RETURNS trigger AS $prevencao_update_tipo_pacifico$
BEGIN

	IF (OLD.tipo_pacifico <> NEW.tipo_pacifico) THEN
		RAISE EXCEPTION 'Não é permitido alterar o tipo de mob pacífico.';
	END IF;
	
	RETURN NEW;
	
END;

$prevencao_update_tipo_pacifico$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER prevencao_update_tipo_pacifico
BEFORE UPDATE ON Pacifico
FOR EACH ROW EXECUTE PROCEDURE prevencao_update_tipo_pacifico();

--- CHECAR EXISTÊNCIA NA TABELA PACIFICO

CREATE OR REPLACE FUNCTION check_existe_pacifico() RETURNS trigger AS $check_existe_pacifico$
BEGIN
	PERFORM * FROM Pacifico WHERE nome_mob = NEW.nome_mob;
	IF FOUND THEN
		RAISE EXCEPTION 'Este mob já existe na tabela Pacifico.';
	END IF;
	
	RETURN NEW;
END;
$check_existe_pacifico$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER check_existe_pacifico
BEFORE INSERT ON Agressivo
FOR EACH ROW EXECUTE PROCEDURE check_existe_pacifico();

--- CHECAR EXISTÊNCIA NA TABELA AGRESSIVO

CREATE OR REPLACE FUNCTION check_existe_agressivo() RETURNS trigger AS $check_existe_agressivo$
BEGIN
	PERFORM * FROM Agressivo WHERE nome_mob = NEW.nome_mob;
	IF FOUND THEN
		RAISE EXCEPTION 'Este mob já existe na tabela Agressivo.';
	END IF;
	
	RETURN NEW;
END;
$check_existe_agressivo$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER check_existe_agressivo
BEFORE INSERT ON Pacifico
FOR EACH ROW EXECUTE PROCEDURE check_existe_agressivo();

-- ANALISAR COM BRUNO DEPOIS

CREATE OR REPLACE PROCEDURE inserir_inst_estrutura(
    nome_estrutura VARCHAR,
    nome_bioma VARCHAR,
    numero_chunk INT,
    nome_mapa VARCHAR,
    OUT nova_estrutura_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Inserir a estrutura na tabela InstanciaEstrutura
    INSERT INTO InstanciaEstrutura (nome_estrutura, nome_bioma, numero_chunk, nome_mapa)
    VALUES (nome_estrutura, nome_bioma, numero_chunk, nome_mapa)
    RETURNING id_inst_estrutura INTO nova_estrutura_id;
END;
$$;

CREATE OR REPLACE PROCEDURE inserir_inst_mob(
    nome_mob VARCHAR,
    vida_atual INT,
    numero_chunk INT,
    nome_mapa VARCHAR,
    id_estrutura INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Inserir o mob na tabela InstanciaMob
    INSERT INTO InstanciaMob (nome_mob, vida_atual, numero_chunk, nome_mapa, id_estrutura)
    VALUES (nome_mob, vida_atual, numero_chunk, nome_mapa, id_estrutura);
END;
$$;

CREATE OR REPLACE PROCEDURE inserir_inst_fonte(
    nome_fonte VARCHAR, 
    qtd_atual INT, 
    numero_chunk INT, 
    nome_mapa VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    -- Inserir uma instância de fonte no chunk
    INSERT INTO InstanciaFonte (nome_fonte, qtd_atual, numero_chunk, nome_mapa)
    VALUES (nome_fonte, qtd_atual, numero_chunk, nome_mapa);
END;
$$;

CREATE OR REPLACE PROCEDURE inserir_inst_construivel(
    nome_construivel VARCHAR,
    numero_chunk INT,
    nome_mapa VARCHAR
)
LANGUAGE plpgsql AS
$$
BEGIN
    -- Inserir instância do construível
    INSERT INTO InstanciaConstruivel (nome_construivel, numero_chunk, nome_mapa)
    VALUES (nome_construivel, numero_chunk, nome_mapa);
END;
$$;
