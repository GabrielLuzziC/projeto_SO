# Nome do executável final
APP_NAME = app

# Caminho do arquivo principal
MAIN_FILE = projetoA/main.py

# Diretórios de saída do PyInstaller
DIST_DIR = dist
BUILD_DIR = build

# Caminho para o Python dentro do seu venv
PYTHON = venv/bin/python3

# Alvo padrão: gerar o executável
all: clean build

# Compila com PyInstaller
build:
	@echo " Gerando executável..."
	@. venv/bin/activate && pyinstaller --onefile --noconsole --name $(APP_NAME) $(MAIN_FILE)
	@echo "✅ Executável criado em $(DIST_DIR)/$(APP_NAME)"

# Limpa arquivos temporários
clean:
	@echo " Limpando arquivos antigos..."
	@rm -rf $(BUILD_DIR) $(DIST_DIR) $(APP_NAME).spec __pycache__

# Executa o app (depois de criado)
run:
	@./$(DIST_DIR)/$(APP_NAME)
