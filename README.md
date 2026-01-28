# basic4web

Biblioteca interna para uso em projetos privados.

## Descrição

basic4web é uma biblioteca Python que fornece funcionalidades comuns e reutilizáveis para projetos internos, incluindo:

- Autenticação e autorização JWT
- Integração com MongoDB
- Integração com RabbitMQ
- Integração com MinIO para armazenamento de objetos
- Suporte a OAuth para Google e Microsoft
- Reconhecimento facial com DeepFace
- Utilidades para processamento de imagens

## Instalação

```bash
pip install -e .
```

## Dependências

Todas as dependências estão listadas em `setup.py`. As principais incluem:

- Flask
- PyJWT
- pymongo
- pika
- minio
- deepface
- OpenCV
- And more...

## Estrutura do Projeto

```
basic4web/
├── controllers/     # Controladores base
├── middleware/      # JWT, logging, socket manager
├── repository/      # Ferramentas para MongoDB, RabbitMQ, MinIO
├── tools/          # OAuth, DeepFace, processamento de imagens
├── common_utils.py # Utilitários comuns
└── config.py       # Configurações base
```

## Autor

**Gustavo Liberatti**

- Email: liberatti.gustavo@gmail.com
- GitHub: [@liberatti](https://github.com/liberatti)

## Licença

MIT License