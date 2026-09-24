# Visibilidade dos pedidos: decisão pendente

Hoje, qualquer usuário autenticado pode listar e consultar todos os pedidos e seus itens. A criação de pedidos e itens também exige JWT, mas os registros não têm vínculo com um usuário. Esse comportamento foi mantido nesta revisão.

Tornar pedidos privados exige uma decisão de produto sobre propriedade e acesso. Para aplicar a regra, será necessário adicionar o proprietário ao pedido, associá-lo ao usuário do token na criação, definir o tratamento dos pedidos já existentes e filtrar tanto as consultas de pedidos quanto as de itens. A mudança altera as respostas observáveis da API e pede novos testes de autorização e atualização do Swagger.
