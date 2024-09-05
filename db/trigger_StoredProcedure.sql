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

--- REMOVE A PERMISSÃO DE DELETAR DIRETAMENTE NAS TABELAS

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