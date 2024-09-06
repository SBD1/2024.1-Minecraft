-- Criação do novo usuário
CREATE ROLE minecraft_user WITH LOGIN PASSWORD 'password';

-- Conceder permissões ao novo usuário
GRANT ALL PRIVILEGES ON DATABASE "2024_1_Minecraft" TO minecraft_user;
