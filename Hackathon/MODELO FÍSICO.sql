create database nufinancas;
use nufinancas;

create table financas(
	idtransacao int,
    idcliente int,
    tipotransacao varchar (20),
    valor decimal (10,2),
    datatransacao date,
    horatransacao time,
    categoria varchar (50),
    descricao varchar (150),
    saldopostransacao decimal (10,2),
    metodopagamento varchar (20),
    primary key (idtransacao,idcliente)
    );


insert into financas(idtransacao,idcliente,tipotransacao,valor,datatransacao,horatransacao,categoria,descricao,saldopostransacao,metodopagamento)
values (1,101,'débito','150.00','2024-07-20','14:35','alimentação','Restaurante japonês','2850.00','cartão'),
(2,102,'crédito','3000.00','2024-07-19','09:20','Salário','Salario Mensal','4200.00','TED'),
(3,101,'débito','50.00','2024-07-18','18:45','transporte','corrida de aplicativo','2900.00','Cartão'),
(4,103,'débito','200.00','2024-07-17','16:10','lazer','cinema e pipoca','1850.00','boleto'),
(5,104,'débito','500.00','2024-07-16','10:50','educação','Curso de Programação','4500.00','cartão'),
(6,102,'débito','250.00','2024-07-15','12:00','compras','Loja de roupas','3950.00','cartão');

create view relatorio_transacoes AS
SELECT idtransacao, idcliente, valor, saldopostransacao,tipotransacao,metodopagamento
FROM financas
WHERE tipotransacao = 'débito';

drop view relatorio_transacoes;

select * from relatorio_transacoes;